from subprocess import run, check_output
from os import path
from os import walk

# Import classes
from classes.attacker import Attacker
from classes.defender import Defender

from classes.global_variables import *

"""
Main file for handling everything by calling other classes in desired way

Place program to be played on in /generation/src/'code file'
"""

# Instances of attacker and defender
attacker = Attacker()
defender = Defender()


# Generate sets for mutants and tests
#
# Parameters:
#     program: name of the program, eg. Name.java
#
# Returns:
#     nothing

def generate_sets():
    if path.isdir('../generation/mutants') == 0:
        attacker.generate_mutants()
    if path.isdir('../generation/evosuite-tests') == 0:
        defender.generate_tests()


# Do testing on selected mutants by a set of selected tests
def execute_testing(testing_set):
    test_class = TESTS_FOLDER_NAME + '.' + TESTS_FILE_NAME[:-5]
    test_case = ','.join(testing_set)

    run(['./run_tests.sh', test_class, test_case], cwd='../generation/')


# Main function to run it all
def main():
    # Generate mutants and tests for a given program
    generate_sets()

    # print(attacker.m_subset.excluded_sorted_ids)
    # attacker.m_subset.create_exclude_ids_file()
    # print(defender.t_subset.tests_ids)

    execute_testing(defender.t_subset.tests_ids)
    # print(TESTS_FILE_NAME)
    # print(TESTS_FOLDER_NAME)
    # print(TESTS_FOLDER_NAME + '.' + TESTS_FILE_NAME[:-5])


if __name__ == "__main__":
    main()
