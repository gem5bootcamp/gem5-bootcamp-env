if __name__ == "__m5_main__":
    # write to a file
    with open("example.txt", "w") as output_file:
        for i in range(10):
            output_file.write(
                f"{i}\n"
            )  # the write function does not emit "\n" by default

    # read from a file
    with open("example.txt", "r") as input_file:
        for line in input_file.readlines():  # read all lines from the input file
            line = line.strip()  # strip the \n character of each line
            print(line)

    # add more content to a file
    with open("example.txt", "a") as output_file:
        for i in range(10, 16):
            output_file.write(f"{i}\n")
