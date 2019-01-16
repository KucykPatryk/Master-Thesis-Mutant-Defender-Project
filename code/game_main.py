# Import classes
from classes.attacker import Attacker
#from classes.defender import Defender

"""
Main file for handling everything by calling other classes in desired way

Place program to be played on in /generation/src/'code file'
"""

# Instances of attacker and defender
attacker = Attacker()
#defender = Defender()


"""
Generate sets for mutants and tests

Parameters:
    program: name of the program, eg. Name.java

Returns:
    nothing
"""


def generate_sets():
    attacker.generate_mutants()
    # defender.generate_tests()


# Main function to run it all
def main():
    # TODO write the function

    # Generate mutants and tests for a given program
    generate_sets()

    # Read the generated files


if __name__ == "__main__":
    main()
