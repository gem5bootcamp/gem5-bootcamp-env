# Notes for the simple events section

## Copy in the template

From `materials/Developing gem5 models/03-events` to `src/tutorial`

## Events

### `my_hello_object.hh`

```c++
    class MyHelloObject : public SimObject
{
  private:
    void processEvent();

    EventFunctionWrapper event;
```

- Add a function to execute on the event
- Add an event (just a simple function wrapper)

- Notice that we're also going to use the startup function.
- Also notice the new variable latency and timesleft

### `my_hello_object.cc`

```c++
MyHelloObject::MyHelloObject(const Params &params) :
    SimObject(params),
    event([this]{ processEvent(); }, name() + ".event"),
    myName("silly-name-for-my-hello-object"),
    latency(1000),
    timesLeft(10)
```

- Initialize things
- Talk about the lambda-ness going on with the event

```c++
void
MyHelloObject::processEvent()
{
    timesLeft--;
    DPRINTF(MyHelloExample, "Hello world! Processing the event! %d left\n",
                          timesLeft);

    if (timesLeft <= 0) {
        DPRINTF(MyHelloExample, "Done firing!\n");
        goodbye->sayGoodbye(myName);
    } else {
        schedule(event, curTick() + latency);
    }
}
```

- Do something interesting

```c++
void
MyHelloObject::startup()
{
    // Before simulation starts, we need to schedule the event
    schedule(event, latency);
}
```

- Kick things off

### `SConscript`

```python
SimObject('MyHelloObject.py', sim_objects=['MyHelloObject'])
```

### Build it and run it

```sh
scons -j17 build/NULL/gem5.opt
```

- Copy the runscript out of `materials/Developing gem5 models/03-events/run_hello_goodbye.py`

```sh
build/NULL/gem5.opt --debug-flags=MyHelloExample run_hello_goodbye.py
```

## Adding parameters

### `MyHelloObject.py`

```python
class MyHelloObject(SimObject):
    type = 'MyHelloObject'
    cxx_header = "tutorial/my_hello_object.hh"
    cxx_class = 'gem5::MyHelloObject'

    time_to_wait = Param.Latency("Time before firing the event")
    number_of_fires = Param.Int(1, "Number of times to fire the event before "
                                   "goodbye")
```

### `my_hello_object.cc`

```c++
    // Note: This is not needed as you can *always* reference this->name()
    myName(params.name),
    latency(params.time_to_wait),
    timesLeft(params.number_of_fires)
```

### REBUILD

```sh
scons -j17 build/NULL/gem5.opt
```

### Show it fails

```sh
build/NULL/gem5.opt --debug-flags=MyHelloExample run_hello_goodbye.py
```

### `run_hello_goodbye.py`

```python
# Create an instantiation of the simobject you created
root.hello = MyHelloObject(
    time_to_wait = '1.5ns',
)
root.hello.number_of_fires = 7
```

- Add parameters to the python config
- Can do it in the constructor (by named parameter) or by setting the member value
- Must have values before instantiate for any parameters without defaults.

### Run again

```sh
build/NULL/gem5.opt --debug-flags=MyHelloExample run_hello_goodbye.py
```

## Two simobjects

### `MyHelloObject.py`

```python
class MyHelloObject(SimObject):
    type = 'MyHelloObject'
    cxx_header = "tutorial/my_hello_object.hh"
    cxx_class = 'gem5::MyHelloObject'

    time_to_wait = Param.Latency("Time before firing the event")
    number_of_fires = Param.Int(1, "Number of times to fire the event before "
                                   "goodbye")

    goodbye_object = Param.MyGoodbyeObject("A goodbye object")
```

- Talk about what MyGoodbyeObject is going to be doing
- We're going to repeat a message until it fills a buffer.
- We are going to have a fixed buffer size and a bandwidth that the buffer can be filled.

```python
class MyGoodbyeObject(SimObject):
    type = 'MyGoodbyeObject'
    cxx_header = "tutorial/my_goodbye_object.hh"
    cxx_class = 'gem5::MyGoodbyeObject'

    buffer_size = Param.MemorySize('1kB',
                                   "Size of buffer to fill with goodbye")
    write_bandwidth = Param.MemoryBandwidth('100MB/s', "Bandwidth to fill "
                                            "the buffer")
```

### `my_hello_object.hh`

- Remove default value for goodbye

### `my_hello_object.cc`

```c++
MyHelloObject::MyHelloObject(const Params &params) :
    SimObject(params),
    // This is a C++ lambda. When the event is triggered, it will call the
    // processEvent() function. (this must be captured)
    event([this]{ processEvent(); }, name() + ".event"),
    goodbye(params.goodbye_object),
```

```c++
void
MyHelloObject::processEvent()
{
    timesLeft--;
    DPRINTF(MyHelloExample, "Hello world! Processing the event! %d left\n",
                          timesLeft);

    if (timesLeft <= 0) {
        DPRINTF(MyHelloExample, "Done firing!\n");
        goodbye->sayGoodbye(myName);
    } else {
        schedule(event, curTick() + latency);
    }
```

### `my_goodbye_object.cc`

- Talk about creating a new buffer and making sure to delete it.
  - Try not to use new like this...

- Look at implementation of `sayGoodbye`. It kicks off the first fill buffer when it happens
  - Note: there's no latency between when hello calls goodbye and when the first stuff shows up in the buffer.

```c++
void
MyGoodbyeObject::fillBuffer()
{
    // There better be a message
    assert(message.length() > 0);

    // Copy from the message to the buffer per byte.
    int bytes_copied = 0;
    for (auto it = message.begin();
         it < message.end() && bufferUsed < bufferSize - 1;
         it++, bufferUsed++, bytes_copied++) {
        // Copy the character into the buffer
        buffer[bufferUsed] = *it;
    }

    if (bufferUsed < bufferSize - 1) {
        // Wait for the next copy for as long as it would have taken
        DPRINTF(MyHelloExample, "Scheduling another fillBuffer in %d ticks\n",
                bandwidth * bytes_copied);
        schedule(event, curTick() + bandwidth * bytes_copied);
    } else {
        DPRINTF(MyHelloExample, "Goodbye done copying!\n");
        // Be sure to take into account the time for the last bytes
        exitSimLoop(buffer, 0, curTick() + bandwidth * bytes_copied);
    }
}
```

- Count the bytes copied so we can delay that long based on the bandwidth
  - Can't just assume the size of the message
- Copy the message into the buffer
- If the buffer isn't full, then we need to do this again, but we need to delay based on the bandwidth
- If the buffer is full, then we can exit the simulation loop

### `SConscript`

```python
SimObject('MyHelloObject.py', sim_objects=['MyHelloObject', 'MyGoodbyeObject'])
```

### REBUILD

```sh
scons -j17 build/NULL/gem5.opt
```

### `run_hello_goodbye.py`

```python
root.hello = MyHelloObject(
    time_to_wait = '1.5ns',
)
root.hello.number_of_fires = 7
root.hello.goodbye_object = GoodbyeObject()
```

- Add the parameter for the goodbye object

### Run again

```sh
build/NULL/gem5.opt --debug-flags=MyHelloExample run_hello_goodbye.py
```

- Vary a parameter for the Goodbye object

```python
root.hello.goodbye_object = GoodbyeObject(bandwidth='10KiB')
```

```sh
build/NULL/gem5.opt --debug-flags=MyHelloExample run_hello_goodbye.py
```

- there should be a different output
