if __name__ == "__m5_main__":
    # for loop
    print("for loop")
    for i in range(5):
        print("i =", i)
    print()

    # using for loop to traverse a list with index
    print("for loop with enumrate")
    my_list = ["a", "b", "c", "d", "e"]
    for index, element in enumerate(my_list):
        print("index =", index, ", element =", element)
    print()

    # while loop
    print("while loop")
    x = 0
    while x < 3:
        print("x =", x)
        x += 1
    print()

    # if statement
    print("if statement")
    y = 3
    if y > 0:
        print("y > 0")
    else:
        print("y <= 0")

    # another way of using if statement
    x = "y equals to 0" if y == 0 else "y is not zero"
    print(x)
