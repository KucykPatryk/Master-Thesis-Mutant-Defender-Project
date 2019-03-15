from subprocess import run
from os import path, rename
import random
import csv
import matplotlib.pyplot as plt
import numpy as np
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


def generate_sets():
    """ Generate sets for mutants and tests """
    if path.isdir('../generation/mutants') == 0:
        attacker.generate_mutants()
    if path.isdir('../generation/evosuite-tests') == 0:
        defender.generate_tests()


def execute_testing(testing_set):
    """ Do testing on selected mutants by a set of selected tests """
    test_class = TESTS_FOLDER_NAME + '.' + TESTS_FILE_NAME[:-5]
    test_case = ','.join(['test' + e for e in testing_set])
    print(test_case)

    run(['./run_tests.sh', test_class, test_case], cwd='../generation/')


def update_results():
    """ Updating results after last round """
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


def cov_map_dic(file_path='../generation/covMap.csv'):
    """ Save and store covered mutants by tests in a dictionary,
    where key is test id and value is an array of mutant ids """
    cov_tests = dict()

    with open(file_path) as cv:
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


def delete_rand_items(items, n):
    """ Randomly deletes n items from a list """
    to_delete = set(random.sample(range(len(items)), n))
    return [x for i, x in enumerate(items) if i not in to_delete]


def produce_mutants_features(ids, mc_dict):
    """ Produces mutants features string
    :param ids: mutant ids as list
    :param mc_dict: dictionary created from mutation.context file
    :return: dictionary created from mutation.context file
    """
    mf = ''
    for row in mc_dict:
        if row['mutantNo'] in ids:
            # mf += row['mutantNo'] + '| '
            mf += '| '
            mf += row['mutationOperatorGroup'] + ':1.0 '
            index = row['mutationOperator'].index(':')
            if row['mutationOperator'][0] == '<':  # Remove < signs
                mf += row['mutationOperator'][1:index - 1] + row['mutationOperator'][index + 2:-1] + ':1 '
            else:
                mf += row['mutationOperator'][:index] + row['mutationOperator'][index + 1:] + ':1.0 '
            mf += row['nodeTypeBasic'] + ':1.0 '
            index = row['parentContextDetailed'].index(':')
            mf += row['parentContextDetailed'][:index] + row['parentContextDetailed'][index + 1:] + ':1.0 '
            if ':' in row['parentStmtContextDetailed']:
                index = row['parentStmtContextDetailed'].index(':')
                mf += \
                    row['parentStmtContextDetailed'][:index] + row['parentStmtContextDetailed'][index + 1:] + ':1.0 '
            else:
                mf += row['parentStmtContextDetailed'] + ':1 '
            if row['hasVariableChild'] == '1':
                mf += 'hasVariableChild' + ':1.0'
            elif row['hasOperatorChild'] == '1':
                mf += 'hasOperatorChild' + ':1.0'
            elif row['hasLiteralChild'] == '1':
                mf += 'hasLiteralChild' + ':1.0'
            mf += '\n'
    mf = mf[:-1]
    return mf


def filter_tests(cov_map, test_mapping):
    """ Filter out tests that do not cover any mutants from the subset"""
    filtered_t_ids = list()
    for t in cov_map:
        for m in attacker.m_subset.mutants_ids:
            if int(m) in cov_map[t]:
                filtered_t_ids.append(t)
                break
    # Filtered subset for tests
    randomized_filtered_t_ids = delete_rand_items(filtered_t_ids, len(filtered_t_ids) - TESTS_SUBSET_SIZE)

    # Map test number ids to name ids
    for i in range(TESTS_SUBSET_SIZE):
        randomized_filtered_t_ids[i] = test_mapping[randomized_filtered_t_ids[i]]

    return randomized_filtered_t_ids


def plot_results(display, save):
    """ Plot results, and display, or save them as png files"""
    # Plot score for mutants and tests
    x = np.arange(1, attacker.m_set.mutants_count + 1, 1)
    m = [m.score.points for m in attacker.m_set.mutants]
    x2 = np.arange(1, defender.t_suite.tests_count + 1, 1)
    t = [t.score.points for t in defender.t_suite.tests]

    fig, ax = plt.subplots()
    ax.bar(x, m)

    ax.set(xlabel='Mutant', ylabel='Score',
           title='Final scores for mutants')
    ax.grid(axis='y')

    fig2, ax = plt.subplots()
    ax.bar(x2, t)
    ax.set(xlabel='Test', ylabel='Score',
           title='Final scores for tests by their test method number')
    ax.grid(axis='y')

    if save:
        fig.savefig("Mutants.png")
        fig2.savefig("Tests.png")
    if display:
        plt.show()


def main():
    """ Main function to run it all """

    ''' Generate and create main parts before the loop '''
    # Generate mutants and tests for a given program
    generate_sets()

    # Generate coverage map for filtering before the game starts
    cm_path = '../generation/covMap-' + TESTS_FOLDER_NAME + '.csv'
    tm_path = '../generation/testMap-' + TESTS_FOLDER_NAME + '.csv'
    if path.isfile(cm_path) == 0:
        execute_testing(defender.t_suite.tests_ids)
        # Change name, so next time same program runs, it will not be necessary, to run the execution again
        rename('../generation/covMap.csv', cm_path)
        rename('../generation/testMap.csv', tm_path)

    test_mapping = test_map_array(tm_path)
    cov_map = cov_map_dic(cm_path)

    # Read the mutant context information and store it in a dictionary for each row
    mc = open('../generation/mutants.context')
    mc_dict = csv.DictReader(mc)

    ''' !-!-!-!-!-!-!-!-!-! Game is running !-!-!-!-!-!-!-!-!-! '''
    for x in range(GAME_ITERATIONS):
        print("ROUND: ", x)
        # Select random subset for mutants
        if x > 0:
            attacker.m_subset = attacker.new_subset()

        # Create filtered subset for tests
        defender.t_subset = defender.new_subset(defender.t_suite.create_subset(filter_tests(cov_map, test_mapping)))

        if not RANDOM_SELECTION:  # Bandit agents
            ''' Calculate features '''
            # Mutant features
            mutants_features = produce_mutants_features(attacker.m_subset.mutants_ids, mc_dict)
            # print(mutants_features)

            # Test features

            # Model selects the tests and mutants
            m_pred = attacker.vw_mutant.predict(mutants_features)
            # print(m_pred)

            # Execute
            execute_testing(defender.t_subset.tests_ids)

            # Update results
            update_results()

            # Model learns
            if x < GAME_ITERATIONS - 1:
                attacker.vw_mutant.learn()
        else:  # Random selection
            # Execute
            execute_testing(defender.t_subset.tests_ids)

            # Update results
            update_results()

    ''' End of The Game '''
    # Plot results
    plot_results(True, True)

    mc.close()
    if not RANDOM_SELECTION:
        attacker.vw_mutant.stop()


if __name__ == "__main__":
    main()

""" TO DO:
- Bar chart instead of line chart
- Line chart (x for round and y for kill ratio)
- Create a log file for each round per line (wins, losses, scores, kill ratio, how much time to run a round)
- For mutants and tests make files at the end with information:
  - For mutants: add how many times was selected, survived and killed, was in the subset 
  - For tests: how many it killed in total and at least one time, how often it was selected, was in the subset
- Structure the random selection same way as bandits
"""
