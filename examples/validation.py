from parsekeyval import Argument, Arguments


class Options(Arguments):
    minimum: int = Argument(default=0, description="Minimum accepted value")
    maximum: int = Argument(default=10, description="Maximum accepted value")

    def validate(self):
        if self.minimum > self.maximum:
            raise ValueError("minimum cannot be greater than maximum")


def main():
    options = Options.parse()
    print(options)


if __name__ == "__main__":
    main()

# Try it with:
# python examples/validation.py --minimum 2 --maximum 5
#
# This fails validation:
# python examples/validation.py --minimum 10 --maximum 5
