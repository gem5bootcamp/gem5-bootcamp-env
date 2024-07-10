from gem5.resources.resource import obtain_resource

# grep "obtain_resource(.*)" materials/isca24/ -roh | sort | uniq
# note, this does not work for workloads. We have to get the resources used
# in each workload.

obtain_resource("x86-linux-kernel-5.4.0-105-generic").get_local_path()
obtain_resource("x86-m5-exit").get_local_path()
obtain_resource("x86-ubuntu-24.04-npb-img").get_local_path()
obtain_resource("x86-ubuntu-24.04-img").get_local_path()
