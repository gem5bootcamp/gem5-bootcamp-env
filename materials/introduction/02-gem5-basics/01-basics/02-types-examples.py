if __name__ == "__m5_main__":
    a = 123  # int
    print("L1:", a)
    print("L2:", type(a))
    print()

    b = "hello"  # string (immutable)
    print("L3:", b)
    print("L4:", type(b))
    print()

    my_list = ["a", "b", "c"]  # list
    print("L5:", my_list)
    print("L6:", type(my_list))
    print("L7:", my_list[0])  # print the first element
    print("L8:", my_list[2])  # print the third element
    print("L9:", my_list[-1])  # print the last element
    print("L10:", "list_size:", len(my_list))  # print the size of the list
    my_list.append(987)  # adding new a element to the end of the list
    print("L11:", my_list)
    print()

    my_dictionary = {"x": 1, "y": 2, "z": 3}  # dictionary {key: val}
    print("L12:", my_dictionary)
    print("L13:", type(my_dictionary))
    print("L14:", my_dictionary["x"])  # print the value corresponding to the key "x"
    print("L15:", "y" in my_dictionary)  # check if the key "y" is in the dictionary
    print("L16:", "a" in my_dictionary)
    print("L17:", "dictionary_size:", len(my_dictionary))
    my_dictionary[
        456
    ] = "abc"  # adding a new key 456 with a value "abc" to the dictionary
    print("L18:", my_dictionary)
    print()

    my_set = {"t", "u", "v"}  # set {key}
    print("L19:", my_set)
    print("L20:", type(my_set))
    print("L21:", "t" in my_set)  # check if the key "t" is in the set
    print("L22:", "a" in my_set)  # check if the key "a" is in the set
    print("L23:", "set_size:", len(my_set))
    my_set.add(123)  # adding a new key to the set
    print("L24:", my_set)
    print()

    my_tuple = ("p", "q", "r", "s")  # tuple (immutable)
    print("L25:", my_tuple)
    print("L26:", type(my_tuple))
    print("L27:", "tuple_size:", len(my_tuple))
    # my_tuple[1] = 1 # error
