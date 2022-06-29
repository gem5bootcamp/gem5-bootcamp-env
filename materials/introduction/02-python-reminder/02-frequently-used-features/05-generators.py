# generate the first N elements of the Fibonacci sequence
#   fib[k] = fib[k-1] + fib[k-2]
def Fibonacci_1(N):
    fib = [1, 1]
    for i in range(N - 2):
        fib.append(fib[-1] + fib[-2])
    return fib  # return all values at once


def Fibonacci_generator(N):
    a = 0
    b = 1
    for count in range(N):
        a, b = b, a + b
        yield a


if __name__ == "__m5_main__":
    generator_1 = Fibonacci_generator(10)
    print(type(generator_1))
    print("Iterate through all elements")
    for element in generator_1:
        print(element)
    print("Done")

    print("Iterate through all elements again!")
    for element in generator_1:
        print(element)
    print("Done")

    generator_2 = Fibonacci_generator(10)
    print("Casting a generator to a list")
    fib_list = list(generator_2)
    print(fib_list)
