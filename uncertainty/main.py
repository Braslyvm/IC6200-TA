import sys

from probability import calculate_probabilities
from utils import load_data


def validate_args(args):
    """
    Validate command-line arguments and return the input filename.
    """
    if len(args) != 2:
        sys.exit("Usage: python main.py data.csv")

    return args[1]


def print_probabilities(people, probabilities):
    """
    Print gene and trait probabilities for each person.
    """
    for person in people:
        print(f"{person}:")

        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")

            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def main():
    filename = validate_args(sys.argv)
    people = load_data(filename)
    probabilities = calculate_probabilities(people)

    print_probabilities(people, probabilities)


if __name__ == "__main__":
    main()
