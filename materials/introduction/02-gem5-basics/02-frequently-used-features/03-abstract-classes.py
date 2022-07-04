from abc import ABC, abstractmethod


class AbstractCPU(ABC):
    # not all functions have to be abstract
    def to_string(self):
        return vars(self)

    @abstractmethod
    def connectToInstCache(self, inst_cache):
        pass

    @abstractmethod
    def connectToDataCache(self, data_cache):
        pass


class CPUImplementation1(AbstractCPU):
    def __init__(self, freq):
        self.freq = freq
        self.inst_cache = None
        self.data_cache = None

    def connectToDataCache(self, data_cache):
        self.data_cache = data_cache


class SimpleCacheCPU(AbstractCPU):
    def __init__(self, freq):
        self.freq = freq
        self.data_cache = None

    def connectToInstCache(self, inst_cache):
        # we'll use data_cache for caching instructions
        pass

    def connectToDataCache(self, data_cache):
        print("Connecting cpu to data cache")
        self.data_cache = data_cache


class MultipleCacheCPU(AbstractCPU):
    def __init__(self, freq):
        self.freq = freq
        self.inst_cache = None
        self.data_cache = None

    def connectToInstCache(self, inst_cache):
        print("Connecting cpu to inst cache")
        self.inst_cache = inst_cache

    def connectToDataCache(self, data_cache):
        print("Connecting cpu to data cache")
        self.data_cache = data_cache


# Example of using Abstract classes as an interface design pattern.
#
#   - The function initialize_system() will successfully initialize the
# system dispite the difference between SimpleCacheCPU and MultipleCacheCPU.
# This allows the modular design: ideally, we can swap between classes of the
# same abstract class without having to modify the rest of the system.
#
#   - This is possible because we force SimpleCacheCPU and MultipleCacheCPU
# to have both connectToInstCache() and connectToDataCache() implemented.
#
#   - In other words, because the AbstractCPU class provides the guarantee that
# every non-abstract class derived from AbstractCPU has its own implementation
# of connectToInstCache() and connectToDataCache(), we can call those functions
# without knowing whether it is SimpleCacheCPU or MultipleCacheCPU.
class Simulator:
    def __init__(self, cpu, inst_cache, data_cache):
        self.cpu = cpu
        self.inst_cache = inst_cache
        self.data_cache = data_cache

    def initialize_system(self):
        self.cpu.connectToInstCache(self.inst_cache)
        self.cpu.connectToDataCache(self.data_cache)


if __name__ == "__m5_main__":
    # creating an object from an abstract function will cause an error
    try:
        cpu = AbstractCPU()
    except Exception as exception:
        print(type(exception))
        print(exception)
        print()

    # a class having at least one abstract function is an abstract class
    try:
        cpu = CPUImplementation1("4GHz")
    except Exception as exception:
        print(type(exception))
        print(exception)
        print()

    cpu1 = SimpleCacheCPU("4GHz")
    cpu2 = MultipleCacheCPU("2GHz")

    inst_cache = "Inst Cache"
    data_cache = "Data Cache"

    print("Setting up simulator 1")
    simulator1 = Simulator(cpu1, inst_cache, data_cache)
    simulator1.initialize_system()
    print()

    print("Setting up simulator 2")
    simulator2 = Simulator(cpu2, inst_cache, data_cache)
    simulator2.initialize_system()
