class Processor:
    type_name = "Processor"

    def __init__(self, freq):
        self.freq = freq

    def change_type_name(self, new_name):
        self.type_name = new_name  # this does not change Processor.type_name
        # it creates an object variable instead


class ProcessorWithClassFunction(Processor):
    def __init__(self, freq):
        super(ProcessorWithClassFunction, self).__init__(freq)

    @classmethod  # A proper way to update a class variable is to use class methods
    def change_type_name_with_class_function(cls, new_name):
        cls.type_name = new_name


if __name__ == "__m5_main__":
    print("***** Class variable example")

    cpu1 = Processor("1GHz")
    cpu2 = Processor("2GHz")

    print("cpu1 type_name:", cpu1.type_name)
    print("cpu2 type_name:", cpu2.type_name)
    print("Processor type_name:", Processor.type_name)
    print()

    Processor.type_name = "MyProcessor"
    print("cpu1 type_name:", cpu1.type_name)
    print("cpu2 type_name:", cpu2.type_name)
    print("Processor type_name:", Processor.type_name)
    print()

    cpu1.change_type_name("MyProcessor111")
    print("cpu1 type_name:", cpu1.type_name)
    print(vars(cpu1))
    print("cpu2 type_name:", cpu2.type_name)
    print(vars(cpu2))
    print("Processor type_name:", Processor.type_name)
    print()

    cpu2.type_name = "NotProcessor"  # this will create an object variable for cpu2
    print("cpu1 type_name:", cpu1.type_name)
    print(vars(cpu1))
    print("cpu2 type_name:", cpu2.type_name)
    print(vars(cpu2))
    print("Processor type_name:", Processor.type_name)
    print()

    # change the type_name back to the original one
    Processor.type_name = "Processor"

    print("***** Class function example")
    cpu1 = ProcessorWithClassFunction("1GHz")
    cpu2 = ProcessorWithClassFunction("2GHz")
    ProcessorWithClassFunction.change_type_name_with_class_function("NewProcessor")
    print("cpu1 type_name:", cpu1.type_name)
    print("cpu2 type_name:", cpu2.type_name)
    print("ProcessorWithClassFunction type_name:", ProcessorWithClassFunction.type_name)
    print()

    cpu1.change_type_name_with_class_function("NewImprovedProcessor")
    print("cpu1 type_name:", cpu1.type_name)
    print("cpu2 type_name:", cpu2.type_name)
    print("ProcessorWithClassFunction type_name:", ProcessorWithClassFunction.type_name)
