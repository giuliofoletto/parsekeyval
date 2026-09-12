from parsekeyval import Argument, Arguments


class Options(Arguments):
    word: str = Argument(default="hello", description="Word to print")
    number: int = Argument(default=1, description="Number of times to print the word")
    uppercase: bool = Argument(default=False, description="Whether to print the word in uppercase")


def main():
    options = Options.parse()
    print(options)
    print("Printing the word:")
    for _ in range(options.number):
        if options.uppercase:
            print(options.word.upper())
        else:
            print(options.word)


if __name__ == "__main__":
    main()

# Boolean values can be passed in key-value style:
# python examples/example.py --uppercase true
# python examples/example.py --uppercase false
#
# Convenience flag aliases are also available:
# python examples/example.py --uppercase
# python examples/example.py --no-uppercase
