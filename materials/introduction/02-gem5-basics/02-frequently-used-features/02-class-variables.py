class Processor:
    default_frequency = "3GHz"

    def __init__(self, name):
        self.name = name

    def change_default_frequency(self, new_frequency):
        # this does not change Processor.default_frequency
        # it creates an *object* variable instead
        self.default_frequency = new_frequency

    def to_string(self):
        return str(vars(self))


class ProcessorWithClassFunction(Processor):
    def __init__(self, name):
        super().__init__(name)

    @classmethod  # A proper way to update a class variable is to use class methods
    def change_default_frequency_with_class_function(cls, new_frequency):
        cls.default_frequency = new_frequency


if __name__ == "__m5_main__":
    cpu1 = Processor("Processor 1")
    cpu2 = Processor("Processor 2")

    print("***** Class variable example 1: Accessing a class variable")
    print(f"Accessing default_frequency via cpu1: {cpu1.default_frequency}")
    print(f"Accessing default_frequency via cpu2: {cpu2.default_frequency}")
    print(f"Accessing default_frequency via Processor: {Processor.default_frequency}")
    print()

    Processor.default_frequency = "1GHz"
    print("***** Class variable example 2: Directly changing a class variable")
    print(f"Accessing default_frequency via cpu1: {cpu1.default_frequency}")
    print(f"Accessing default_frequency via cpu2: {cpu2.default_frequency}")
    print(f"Accessing default_frequency via Processor: {Processor.default_frequency}")
    print()

    cpu1.default_frequency = "200MHz"  # this will create an object variable for cpu2 1
    print("***** Class variable example 3: Mistakenly creating an object variable")
    print(f"Accessing default_frequency via cpu1: {cpu1.default_frequency}")
    print(f"Accessing default_frequency via cpu2: {cpu2.default_frequency} (why?)")
    print(
        f"Accessing default_frequency via Processor: {Processor.default_frequency} (why?)"
    )
    print()
    print(f"cpu1 object variables: {vars(cpu1)}")
    print(f"cpu2 object variables: {vars(cpu2)}")
    print()

    cpu2.change_default_frequency("800MHz")
    print("***** Class variable example 4: Mistakenly creating an object variable")
    print(f"Accessing default_frequency via cpu1: {cpu1.default_frequency} (why?)")
    print(f"Accessing default_frequency via cpu2: {cpu2.default_frequency} (why?)")
    print(
        f"Accessing default_frequency via Processor: {Processor.default_frequency} (why?)"
    )
    print()
    print(f"cpu1 object variables: {vars(cpu1)}")
    print(f"cpu2 object variables: {vars(cpu2)}")
    print()

    # change the default_frequency back to the original one
    Processor.default_frequency = "3GHz"

    cpu1 = ProcessorWithClassFunction("ProcessorWithClassFunction 1")
    cpu2 = ProcessorWithClassFunction("ProcessorWithClassFunction 2")

    print(
        "***** Class function example 5: Changing a class variable via a class function"
    )
    ProcessorWithClassFunction.change_default_frequency_with_class_function("3.5GHz")
    print(f"Accessing default_frequency via cpu1: {cpu1.default_frequency}")
    print(f"Accessing default_frequency via cpu2: {cpu2.default_frequency}")
    print(f"Accessing default_frequency via Processor: {Processor.default_frequency}")
    print(
        f"Accessing default_frequency via ProcessorWithClassFunction: {ProcessorWithClassFunction.default_frequency}"
    )
    print(f"cpu1 object variables: {vars(cpu1)}")
    print(f"cpu2 object variables: {vars(cpu2)}")
    print()

    print(
        "***** Class function example 6: Changing a class variable via a class function"
    )
    cpu1.change_default_frequency_with_class_function("4.5GHz")
    print(f"Accessing default_frequency via cpu1: {cpu1.default_frequency}")
    print(f"Accessing default_frequency via cpu2: {cpu2.default_frequency}")
    print(f"Accessing default_frequency via Processor: {Processor.default_frequency}")
    print(
        f"Accessing default_frequency via ProcessorWithClassFunction: {ProcessorWithClassFunction.default_frequency}"
    )
    print(f"cpu1 object variables: {vars(cpu1)}")
    print(f"cpu2 object variables: {vars(cpu2)}")
    print()
