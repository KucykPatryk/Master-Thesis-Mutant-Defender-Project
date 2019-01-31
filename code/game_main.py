from subprocess import run
from os import path

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


# Updating results after last round
def update_results():
    attacker_won = True

    with open('../generation/summary.csv') as f:
        f.readline()
        summary = f.readline().split(',')

    if int(summary[2]) / int(summary[1]) > WINNING_THRESHOLD:
        attacker_won = False

    with open('../generation/killMap.csv') as f2:
        f2.readline()
        tests = list()  # a list of test ids that killed a mutant
        mutants = list()  # a list of mutant ids that were killed
        for i in range(int(summary[2])):
            line = f2.readline().split(',')
            tests.append(line[0])
            mutants.append((line[1]))

    attacker.update(attacker_won, summary, mutants)
    defender.update(not attacker_won, summary[2], tests)


# Main function to run it all
def main():
    # Generate mutants and tests for a given program
    generate_sets()
    # execute_testing(defender.t_subset.tests_ids)
    update_results()


if __name__ == "__main__":
    main()
