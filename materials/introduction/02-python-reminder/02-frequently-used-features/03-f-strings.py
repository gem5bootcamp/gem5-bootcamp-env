from math import log2

if __name__ == "__m5_main__":
    print("Formatted strings (f-strings)")

    print("Example 1")
    x = 1
    y = 2
    s = f"x = {x}, y = {y}"  # typical use of f-strings
    print(s)
    print()

    print("Example 2")
    print(f"log2(64) = {log2(64)}")
