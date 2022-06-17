# Notes for the simple simobj section

## A simple simobject

### Start building!

```sh
scons -j17 build/NULL/gem5.opt
```

### `MySimpleObject.py`

- `mkdir src/tutorial`
- BTW, I'm going to use "MY..." for everything because names will clash otherwise.

```python
from m5.params import *
from m5.SimObject import SimObject

class MySimpleObject(SimObject):
    type = "MySimpleObject"
    cxx_header = "tutorial/my_simple_object.hh"
    cxx_class = "gem5::MySimpleObject"
```

- This isn't only a python file... it's interpreted by the gem5 build system
- You can create these files when you are creating a SimObject, and if you are *changing a model*. However, you shouldn't modify this to change the value of a parameter
- Need to tell gem5 where to find things to get the model
- This is the magic C++/python glue

### `my_simple_object.hh`

```C++
#ifndef __TUTORIAL_MY_SIMPLE_OBJECT_HH__
#define __TUTORIAL_MY_SIMPLE_OBJECT_HH__

#include "params/MySimpleObject.hh"
#include "sim/sim_object.hh"

namespace gem5
{

class MySimpleObject : public SimObject
{
  public:
    PARAMS(MySimpleObject);
    MySimpleObject(const Params &p);
};

} // namespace gem5

#endif // __TUTORIAL_MY_SIMPLE_OBJECT_HH__
```

- include `sim_object.hh`
- Inherit from `SimObject`
- Make sure you're in the `gem5` namespace!
- `ifndef` for circular dependencies (silly C++)
- `PARAMS` is a convenience function
- The constructor *MUST* follow this signature (or crazy errors happen)
  - Can I show this error?

### `my_simple_object.cc`

```C++
#include "tutorial/my_simple_object.hh"

#include <iostream>

namespace gem5
{

MySimpleObject::MySimpleObject(const Params &params) :
    SimObject(params)
{
    std::cout << "Hello World! From a SimObject!" << std::endl;
}

} // namespace gem5
```

- Don't use `cout` ever... but for now it's ok.
- Make sure to call the parent's constructor with the params

### `SConscript`

```python
Import('*')

SimObject('MySimpleObject.py', sim_objects=['MySimpleObject'])

Source('my_simple_object.cc')
```

- This is the place where we tell the gem5 build system what to compile
- Need to declare that there's a new model (SimObject)
- Need to actually compile the C file

### Start building

```sh
scons -j17 build/NULL/gem5.opt
```

### `run_simple.py`

```python
import m5

from m5.objects import *

root = Root(full_system=False)

root.hello = MySimpleObject()

m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
```

- import the m5 (gem5) library created when gem5 is built
- import all of the SimObjects
- set up the root SimObject and start the simulation
- Create an instantiation of the simobject you created
- instantiate all of the objects we've created above
- Don't forget, this is just a python file, you can do whatever you want in python

### Let's run it!

```sh
build/NULL/gem5.opt run_simple.py
```

## Debugging

### `SConscript`

```python
DebugFlag('MyHelloExample')
```

- Tell gem5 to create a new debug flag
- Debug flags are so that you don't print all debugging all the time.

### `my_simple_object.cc`

```C++
#include "debug/MyHelloExample.hh"

MySimpleObject::MySimpleObject(const Params &params) :
    SimObject(params)
{
    DPRINTF(MyHelloExample, "Created the hello object\n");
}
```

- Include the auto-generated header (yeah, there's a lot of auto-generated code in gem5)
- Then we can use DPRINTF!
- Format string can be anything that's formattable with C

### BUILD AND RUN!

Now we can build and run it

```sh
build/NULL/gem5.opt run_simple.py
```

Oops, that was nothing!

```sh
build/NULL/gem5.opt --debug-flags=MyHelloExample run_simple.py
```

