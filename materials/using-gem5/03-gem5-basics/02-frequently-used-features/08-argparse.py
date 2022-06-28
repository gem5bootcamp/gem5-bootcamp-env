# Documentation: https://docs.python.org/3/library/argparse.html

import argparse

if __name__ == "__main__":
    # Constructing the argument parser
    parser = argparse.ArgumentParser(description="Print arguments.")
    parser.add_argument("argument1", type=int, help="First argument")
    parser.add_argument("--argument2", type=str, help="Second argument")

    # Creating the argument parser object
    args = parser.parse_args()

    # Getting argument 1
    argument1 = args.argument1
    print("argument1")
    print(argument1)
    print(type(argument1))

    # Getting argument 2
    argument2 = args.argument2
    print("argument2")
    print(argument2)
    print(type(argument2))
