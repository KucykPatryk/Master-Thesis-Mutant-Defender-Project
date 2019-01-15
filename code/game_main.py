# Import classes
from classes.attacker import Attacker
from classes.defender import Defender

"""
Main file for handling everything by calling other classes in desired way
"""

# The name of desired program
program_name = 'Triangle.java'

# Instances of attacker and defender
attacker = Attacker()
defender = Defender()


"""
Generate sets for mutants and tests

Parameters:
    program: name of the program, eg. Name.java

Returns:
    nothing
"""


def generate_sets(program):
    attacker.generate_mutants()
    # defender.generate_tests()


# Main function to run it all
def main():
    # TODO write the function

    # Generate mutants and tests for a given program
    generate_sets(program_name)

    # Read the generated files


if __name__ == "__main__":
    main()
