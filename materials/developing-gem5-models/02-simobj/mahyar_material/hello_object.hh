// TODO: License goes here
#ifndef __BOOTCAMP_GEM5_HELLO_OBJECT_HH__
#define __BOOTCAMP_GEM5_HELLO_OBJECT_HH__

#include "params/HelloObject.hh"
#include "sim/sim_object.hh"

namespace gem5
{

class HelloObject : public SimObject
{
  public:
    PARAMS(HelloObject);
    HelloObject(const Params &params);

};

} // namespace gem5

#endif // __BOOTCAMP_GEM5_HELLO_OBJECT_HH__