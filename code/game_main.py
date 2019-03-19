from subprocess import run
from os import path, rename
import random
import matplotlib.pyplot as plt
import numpy as np
from time import perf_counter
from csv import DictWriter

# Import classes
from classes.attacker import Attacker
from classes.defender import Defender
from classes.global_variables import *

"""
Main file for handling everything by calling other classes in desired way

Place program to be played on in /generation/src/'code file'
"""

# Instances of attacker and defender

attacker = Attacker('random')
defender = Defender('random')

kill_ratio_plot = list()


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

        kill_ratio_plot.append(kill_ratio)

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

    # Plot kill ratio for each round
    x = np.arange(1, len(kill_ratio_plot) + 1, 1)
    y = kill_ratio_plot

    fig3, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel='Round', ylabel='Kill Ratio',
           title='Linear visualisation of mutants killed by tests ratio per round')
    ax.grid()

    if save:
        fig3.savefig("Kill_ratio.png")
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

    ''' !-!-!-!-!-!-!-!-!-! Game is running !-!-!-!-!-!-!-!-!-! '''
    with open('game_info_log.csv', 'w') as gl:  # For log round writing
        log_line_header = ['Round', 'Winner', 'Loser', 'Kill Ratio', 'Round Time']
        log_line_dic = dict((key, '') for key in log_line_header)
        gl_writer = DictWriter(gl, fieldnames=log_line_header)
        gl_writer.writeheader()

        for x in range(GAME_ITERATIONS):
            time_start = perf_counter()
            print("ROUND: ", x)
            # Select random subset for mutants
            if x > 0:
                attacker.m_subset = attacker.new_subset(MUTANTS_SUBSET_SIZE)

            # Create filtered subset for tests
            defender.t_subset = defender.new_subset(defender.t_suite.create_subset(filter_tests(cov_map, test_mapping)))

            # Set up attacker and defender
            attacker.prepare_for_testing()
            defender.prepare_for_testing()

            # Execute
            execute_testing(defender.t_subset.tests_ids)

            # Update results
            update_results()

            # Learn the models
            if x < GAME_ITERATIONS - 1:
                if attacker.agent_mode is not 'random':
                    attacker.learn()
                if defender.agent_mode is not 'random':
                    defender.learn()
            time_stop = perf_counter()
            elapsed_time = time_stop - time_start  # In seconds
            print("Elapsed time: %.3f sec" % elapsed_time)

            # Save to log file
            log_line_dic['Round'] = '%d' % (x + 1)
            log_line_dic['Winner'] = 'Attacker' if attacker.last_winner else 'Defender'
            log_line_dic['Loser'] = 'Attacker' if defender.last_winner else 'Defender'
            log_line_dic['Kill Ratio'] = '%.3f' % kill_ratio_plot[x]
            log_line_dic['Round Time'] = '%.3f' % elapsed_time
            gl_writer.writerow(log_line_dic)

    ''' End of The Game '''
    # Plot results
    plot_results(True, True)


if __name__ == "__main__":
    main()

""" TO DO:

- Create a log file for each round per line (wins, losses, kill ratio, how much time to run a round)
- For mutants and tests make files at the end with information:
  - For mutants: add how many times was selected, survived and killed, was in the subset 
  - For tests: how many it killed in total and at least one time, how often it was selected, was in the subset


DONE:
- Bar chart instead of line chart
- Structure the random selection same way as bandits
- Line chart (x for round and y for kill ratio)
"""
