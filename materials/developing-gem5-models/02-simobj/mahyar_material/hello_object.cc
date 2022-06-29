// TODO: License goes here.

// FIXME: Ask Jason where in the gem5 directory these codes will go?
#include "learning_gem5/part2/hello_object.hh"

#include <iostream>

namespace gem5
{

HelloObject::HelloObject(const Params &params):
    SimObject(params),
{
    std::cout << "Hello World! From a SimObject (constructor)." << std::endl;
}

} // namespace gem5