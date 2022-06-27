# generate the first 20 elements of the Fibonacci sequence
#   fib[n] = fib[n-1] + fib[n-2]
def Fibonacci_1():
    fib = [1, 1]
    for i in range(8):
        fib.append(fib[-1] + fib[-2])
    return fib  # return all values at once


def Fibonacci_generator():
    a = 1
    b = 1
    for count in range(10):
        if count < 2:
            yield 1
        else:
            a, b = b, a + b
            yield b


if __name__ == "__m5_main__":
    generator_1 = Fibonacci_generator()
    print(type(generator_1))
    print("Iterate through all elements")
    for element in generator_1:
        print(element)
    print("Done")

    print("Iterate through all elements again!")
    for element in generator_1:
        print(element)
    print("Done")

    generator_2 = Fibonacci_generator()
    print("Casting a generator to a list")
    fib_list = list(generator_2)
    print(fib_list)
