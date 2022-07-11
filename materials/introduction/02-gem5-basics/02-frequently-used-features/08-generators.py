import time

# generate the first N elements of the Fibonacci sequence
#   fib[k] = fib[k-1] + fib[k-2]
def Fibonacci_list(N):
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

    print("Calculating the sum of 10**5 Fibonacci numbers using generator")
    start = time.time()
    fib_generator = Fibonacci_generator(10**5)
    fib_sum = sum(fib_generator)
    end = time.time()
    print(f"Elapsed time: {end-start}s")

    print("Calculating the sum of 10**5 Fibonacci numbers using list")
    start = time.time()
    fib_list = Fibonacci_list(10**5)
    fib_sum = sum(fib_list)
    end = time.time()
    print(f"Elapsed time: {end-start}s")

    print("Calculating the sum of 10**6 Fibonacci numbers using generator")
    start = time.time()
    fib_generator = Fibonacci_generator(10**6)
    fib_sum = sum(fib_generator)
    end = time.time()
    print(f"Elapsed time: {end-start}s")

    # This code will consume more than 25GiB of RAM.
    # print("Calculating the sum of 10**6 Fibonacci numbers using list")
    # start = time.time()
    # fib_list = Fibonacci_list(10**6)
    # fib_sum = sum(fib_list)
    # end = time.time()
    # print(f"Elapsed time: {end-start}s")
