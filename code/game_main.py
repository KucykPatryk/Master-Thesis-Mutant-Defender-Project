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
        kill_ratio = int(summary[2])/MUTANTS_SUBSET_SIZE  # The ratio of killed mutants by the tests

    if kill_ratio > WINNING_THRESHOLD:
        attacker_won = False

    with open('../generation/killMap.csv') as f2:
        f2.readline()
        tests = list()  # a list of test ids that killed a mutant
        mutants = list()  # a list of mutant ids that were killed
        for line in f2:
            line = line.split(',')
            tests.append(line[0])
            mutants.append((line[1]))

    attacker.update(attacker_won, summary, mutants, 1 - kill_ratio)
    defender.update(not attacker_won, summary[2], tests, kill_ratio)


# Returns an array of test ids with their actual method ids
def test_map_array():
    tests = [0]

    with open('../generation/testMap.csv') as tm:
        tm.readline()
        for line in tm:
            line = line.split(',')
            tests.append(line[1][25:-2])

    return tests


# Save and store covered mutants by tests in a 2D array, where x is mutant id and y is test id with 0 for uncovered
def cov_map_2d_array():
    cov_tests = [[-1 for x in range(MUTANTS_COUNT + 1)] for y in range(TEST_COUNT + 1)]

    with open('../generation/covMap.csv') as cv:
        cv.readline()

        for line in cv:
            line = line.split(',')
            m = int(line[0])
            t = int(line[1])
            cov_tests[m][t] = t

    return cov_tests


# Main function to run it all
def main():
    # Generate mutants and tests for a given program
    generate_sets()

    # cov_tests = cov_map_2d_array()

    # !-!-!-!-!-!-!-!-!-! Game is running !-!-!-!-!-!-!-!-!-!
    for x in range(GAME_ITERATIONS):
        print("ROUND: ", x)
        # Select random subset for tests and mutants
        if x > 0:
            attacker.m_subset = attacker.new_subset()
            defender.t_subset = defender.new_subset()

        # Filter the tests, so they all cover at least one mutant

        # tests = test_map_array()

        # Calculate features

        # Model selects the tests/mutants

        # Execute
        # execute_testing(defender.t_subset.tests_ids)

        # Update results
        update_results()


if __name__ == "__main__":
    main()
