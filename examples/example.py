from parsekeyval import BaseArguments, Field, parse_arguments


class Arguments(BaseArguments):
    word: str = Field(default="hello", description="Word to print")
    number: int = Field(default=1, description="Number of times to print the word")
    uppercase: bool = Field(default=False, description="Whether to print the word in uppercase")


def main():
    args = parse_arguments(Arguments)
    print(args)
    print("Printing the word:")
    for _ in range(args.number):
        if args.uppercase:
            print(args.word.upper())
        else:
            print(args.word)


if __name__ == "__main__":
    main()
