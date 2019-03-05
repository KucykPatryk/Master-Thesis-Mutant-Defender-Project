from subprocess import run
from os import path
import random
import csv
import copy
from vowpalwabbit import pyvw

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


# Save and store covered mutants by tests in a 2D array, where x is test id and y is mutant id with 0 for uncovered
# def cov_map_2d_array():
#     cov_tests = [[-1 for x in range(MUTANTS_COUNT + 1)] for y in range(TEST_COUNT + 1)]
#
#     with open('../generation/covMap.csv') as cv:
#         cv.readline()
#
#         for line in cv:
#             line = line.split(',')
#             t = int(line[0])
#             m = int(line[1])
#             cov_tests[t][m] = m
#
#     return cov_tests

# Save and store covered mutants by tests in a dictionary, where key is test id and value is an array of mutant ids
def cov_map_dic():
    cov_tests = dict()

    with open('../generation/covMap.csv') as cv:
        cv.readline()

        for line in cv:
            line = line.split(',')
            t = int(line[0])
            m = int(line[1])

            if t in cov_tests:
                cov_tests[t].append(m)
            else:
                cov_tests[t] = [m]

    return cov_tests


# Randomly deletes n items from a list
def delete_rand_items(items, n):
    to_delete = set(random.sample(range(len(items)), n))
    return [x for i, x in enumerate(items) if i not in to_delete]


# Produces mutants features string
#
# Parameters:
#     ids: mutant ids as list
#     mc_dict: dictionary created from mutation.context file
#
# Returns:
#     a concatenated string of mutants features for Vowpal Wabbit
def produce_mutants_features(ids, mc_dict):
    mf = ''
    for row in mc_dict:
        if row['mutantNo'] in ids:
            mf += '| '
            mf += row['mutationOperatorGroup'] + ':1 '
            index = row['mutationOperator'].index(':')
            mf += row['mutationOperator'][:index] + row['mutationOperator'][index + 1:] + ':1 '
            mf += row['nodeTypeBasic'] + ':1 '
            index = row['parentContextDetailed'].index(':')
            mf += row['parentContextDetailed'][:index] + row['parentContextDetailed'][index + 1:] + ':1 '
            if ':' in row['parentStmtContextDetailed']:
                index = row['parentStmtContextDetailed'].index(':')
                mf += \
                    row['parentStmtContextDetailed'][:index] + row['parentStmtContextDetailed'][index + 1:] + ':1 '
            else:
                mf += row['parentStmtContextDetailed'] + ':1 '
            if row['hasVariableChild'] == '1':
                mf += 'hasVariableChild' + ':1'
            elif row['hasOperatorChild'] == '1':
                mf += 'hasOperatorChild' + ':1'
            elif row['hasLiteralChild'] == '1':
                mf += 'hasLiteralChild' + ':1'
            mf += '\n'
    return mf


# Main function to run it all
def main():
    # Generate mutants and tests for a given program
    generate_sets()

    # # Generate coverage map for filtering before the game starts
    # execute_testing(defender.t_suite.tests_ids)
    # test_mapping = test_map_array()
    # cov_map = cov_map_dic()

    # Read the mutant contex information and store it in a dictionary for each row
    mc = open('../generation/mutants.context')
    mc_dict = csv.DictReader(mc)

    # Create the mutant Vowpal Wabbit model
    vw_mutant = pyvw.vw(quiet=True, cb_explore_adf=True, epsilon=0.1)

    # # !-!-!-!-!-!-!-!-!-! Game is running !-!-!-!-!-!-!-!-!-!
    # for x in range(GAME_ITERATIONS):
    #     print("ROUND: ", x)
    #     # Select random subset for mutants
    #     if x > 0:
    #         attacker.m_subset = attacker.new_subset()
    #         # defender.t_subset = defender.new_subset(defender.t_suite.create_random_subset())
    #
    #     # Filter the tests, so they all cover at least one mutant
    #     filtered_t_ids = list()
    #     for t in cov_map:
    #         for m in attacker.m_subset.mutants_ids:
    #             if int(m) in cov_map[t]:
    #                 filtered_t_ids.append(t)
    #                 break
    #     # Filtered subset for tests
    #     randomized_filtered_t_ids = delete_rand_items(filtered_t_ids, len(filtered_t_ids) - TESTS_SUBSET_SIZE)
    #
    #     # Map test number ids to name ids
    #     for i in range(TESTS_SUBSET_SIZE):
    #         randomized_filtered_t_ids[i] = test_mapping[randomized_filtered_t_ids[i]]
    #     # Create filtered test subset
    #     defender.t_subset = defender.new_subset(defender.t_suite.create_subset(randomized_filtered_t_ids))

    # Calculate features

    mutants_features = produce_mutants_features(attacker.m_subset.mutants_ids, mc_dict)
    print(mutants_features)

    # mf = vw_mutant.example('|')



    # Mutant features

    # Test features


    # Model selects the tests/mutants

    # Execute
    # execute_testing(defender.t_subset.tests_ids)

    # Update filters


    # Update results
    #update_results()

    # End of Game
    mc.close()


if __name__ == "__main__":
    main()
