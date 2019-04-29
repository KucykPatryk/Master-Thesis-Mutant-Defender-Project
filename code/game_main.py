import argparse
from subprocess import run
from os import path, rename, makedirs
import random
import matplotlib.pyplot as plt
import numpy as np
from time import perf_counter
from csv import DictWriter
from shutil import copyfile

# Import classes
from classes.attacker import Attacker
from classes.defender import Defender
from classes.global_variables import *

"""
Main file for handling everything by calling other classes in desired way

Place program to be played on in /generation/src/'code file'
"""

# Instances of attacker and defender

attacker = object()
defender = object()

kill_ratio_plot = list()


def change_separate_class_loader(param):
    """ Change the parameter separateClassLoader to true or false"""
    file = '../generation/programs/' + PROGRAM + '/evosuite-tests/' + defender.tests_folder_name + '/' + \
           defender.tests_file_name
    with open(file, 'r') as etc:
        data = etc.readlines()
        for index, line in enumerate(data):
            if line.startswith('@RunWith'):
                old_string = line
                new_string = old_string[:155] + param + old_string[-18:]
                data[index] = new_string
                break
    with open(file, 'w') as etc:
        etc.writelines(data)


def execute_testing(testing_set, file='./run_tests.sh', cov_parm=''):
    """ Do testing on selected mutants by a set of selected tests """
    test_class = defender.tests_folder_name + '.' + defender.tests_file_name[:-5]
    test_case = ','.join(['test' + e for e in testing_set])

    if file == './run_test_coverage.sh':
        run([file, test_class, test_case, cov_parm, PROGRAM], cwd='../generation/')
    else:
        run([file, test_class, test_case, PROGRAM], cwd='../generation/')


def update_results():
    """ Updating results after last round """
    attacker_won = True

    with open('../generation/programs/' + PROGRAM + '/summary.csv') as f:
        f.readline()
        summary = f.readline().split(',')
        kill_ratio = int(summary[2])/MODEL_PICK_LIMIT_M  # The ratio of killed mutants by the tests

        kill_ratio_plot.append(kill_ratio)

    if kill_ratio > WINNING_THRESHOLD:
        attacker_won = False

    with open('../generation/programs/' + PROGRAM + '/killMap.csv') as f2:
        f2.readline()
        tests = list()  # a list of test ids that killed a mutant
        mutants = list()  # a list of mutant ids that were killed
        for line in f2:
            line = line.split(',')
            tests.append(line[0])
            mutants.append((line[1]))

    attacker.update(attacker_won, summary, mutants, kill_ratio)
    defender.update(not attacker_won, summary[2], tests, kill_ratio)


def cov_map_dic(file_path='../generation/programs/' + PROGRAM + '/covMap.csv'):
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


def select_rand_items(items, n):
    """ Randomly returns n items from a list as a list """
    to_delete = set(random.sample(range(len(items)), n))
    return [x for i, x in enumerate(items) if i not in to_delete]


def filter_tests(cov_map, test_mapping, size):
    """ Filter out tests that do not cover any mutants from the subset"""
    filtered_t_dic = dict((key, list()) for key in attacker.m_subset.mutants_ids)
    filtered_t_ids = list()

    for m in attacker.m_subset.mutants_ids:
        for t in cov_map:
            if int(m) in cov_map[t]:
                filtered_t_dic[m].append(t)

    # Filtered subset for tests
    i = 0
    while True:
        for key in filtered_t_dic:
            choice = random.choice(filtered_t_dic[key])
            filtered_t_ids.append(choice)
            i += 1
            if i == size:
                break
        if i == size:
            break

    # Map test number ids to name ids
    for i in range(size):
        filtered_t_ids[i] = test_mapping[filtered_t_ids[i]]

    return filtered_t_ids


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
        fig.savefig('output/' + OUTPUT_RUN_DIR + '/Mutants.png')
        fig2.savefig('output/' + OUTPUT_RUN_DIR + '/Tests.png')
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
        fig3.savefig('output/' + OUTPUT_RUN_DIR + '/Kill_ratio.png')
    if display:
        plt.show()


def update_was_in_subset(subset_ids, agent):
    """ Update was in subset count """
    agent.update_wis(subset_ids)


def save_log_file(x, elapsed_time, writer, log_line_dic):
    """ Writes to log file given round info """
    log_line_dic['Round'] = '%d' % (x + 1)
    log_line_dic['Winner'] = 'Attacker' if attacker.last_winner else 'Defender'
    log_line_dic['Loser'] = 'Attacker' if defender.last_winner else 'Defender'
    log_line_dic['Kill Ratio'] = '%.3f' % kill_ratio_plot[x]
    log_line_dic['Mutants Survived'] = attacker.m_subset.survived
    log_line_dic['Mutants Killed'] = attacker.m_subset.killed
    log_line_dic['Round Time'] = '%.3f' % elapsed_time
    writer.writerow(log_line_dic)


def save_mutants_file():
    """ Produce mutants file with information about them """
    with open('output/' + OUTPUT_RUN_DIR + '/mutants_info.csv', 'w') as mi:
        line_header = ['Mutant Number', 'Score', 'Times Killed', 'Times Survived', 'Times in a Subset',
                       'Times selected by Agent']
        line_dic = dict((key, '') for key in line_header)
        mi_writer = DictWriter(mi, fieldnames=line_header)
        mi_writer.writeheader()
        for m in attacker.m_set.mutants:
            line_dic['Mutant Number'] = m.id
            line_dic['Score'] = '%.3f' % m.score.points
            line_dic['Times Killed'] = m.killed_times
            line_dic['Times Survived'] = m.survived_times
            line_dic['Times in a Subset'] = m.subset_chosen_times
            line_dic['Times selected by Agent'] = m.selected
            mi_writer.writerow(line_dic)


def save_tests_file():
    """ Produce tests file with information about them """
    with open('output/' + OUTPUT_RUN_DIR + '/tests_info.csv', 'w') as ti:
        line_header = ['Test Name', 'Score', 'Times Killed', 'Times in a Subset', 'Times selected by Agent']
        line_dic = dict((key, '') for key in line_header)
        ti_writer = DictWriter(ti, fieldnames=line_header)
        ti_writer.writeheader()
        for t in defender.t_suite.tests:
            line_dic['Test Name'] = 'test' + str((t.id - 1))
            line_dic['Score'] = '%.3f' % t.score.points
            line_dic['Times Killed'] = t.killed_times
            line_dic['Times in a Subset'] = t.subset_chosen_times
            line_dic['Times selected by Agent'] = t.selected
            ti_writer.writerow(line_dic)


def run_tests_coverage():
    for nr in defender.tests_ids:
        execute_testing([nr], './run_test_coverage.sh', nr)


def main():
    """ Main function to run it all """

    if attacker.agent_mode != 'random':
        attacker.encoder = attacker.features_encoder()

    # Create output directory if it does not exist
    if not path.exists('output'):
        makedirs('output')
    if not path.exists('output/' + OUTPUT_RUN_DIR):
        makedirs('output/' + OUTPUT_RUN_DIR)

    # Generate coverage map for filtering before the game starts
    cm_path = '../generation/programs/' + PROGRAM + '/covMap-' + defender.tests_folder_name + '.csv'
    tm_path = '../generation/programs/' + PROGRAM + '/testMap-' + defender.tests_folder_name + '.csv'
    if not path.isfile(cm_path):
        with open('../generation/programs/' + PROGRAM + '/exclude_mutants.txt', 'w') as ef:
            ef.write('')
        execute_testing(defender.t_suite.tests_ids)
        # Change name, so next time same program runs, it will not be necessary, to run the execution again
        rename('../generation/programs/' + PROGRAM + '/covMap.csv', cm_path)
        rename('../generation/programs/' + PROGRAM + '/testMap.csv', tm_path)

    # Make run coverage with JaCoCo possible
    if not path.exists('../generation/programs/' + PROGRAM + '/coverage_reports'):
        change_separate_class_loader('false')
        run(['./compile_tests.sh', PROGRAM], cwd='../generation/')
        makedirs('../generation/programs/' + PROGRAM + '/coverage_reports')
        run_tests_coverage()

        # Change back, so testing with major is possible
        change_separate_class_loader('true')
        run(['./compile_tests.sh', PROGRAM], cwd='../generation/')
        # Fix problem after compile, so major sees the mutants
        run(['./fix_java_ver_compile_problem.sh', PROGRAM], cwd='../generation/')
        shutil.move(path.join("../generation/", "mutants.log"),
                    path.join("../generation/programs/" + PROGRAM + "/", "mutants.log"))

    test_mapping = test_map_array(tm_path)
    cov_map = cov_map_dic(cm_path)

    ''' !-!-!-!-!-!-!-!-!-! Game is running !-!-!-!-!-!-!-!-!-! '''
    with open('output/' + OUTPUT_RUN_DIR + '/game_info_log.csv', 'w') as gl:  # For log round writing
        log_line_header = ['Round', 'Winner', 'Loser', 'Kill Ratio', 'Mutants Survived', 'Mutants Killed', 'Round Time']
        log_line_dic = dict((key, '') for key in log_line_header)
        gl_writer = DictWriter(gl, fieldnames=log_line_header)
        gl_writer.writeheader()

        for x in range(GAME_ITERATIONS):
            time_start = perf_counter()
            print("ROUND: ", x)

            # Select random subset for mutants
            if x > 0:
                attacker.m_subset = attacker.new_subset(attacker.m_set, MUTANTS_SUBSET_SIZE)
            update_was_in_subset(attacker.m_subset.mutants_ids, attacker)

            # Create filtered subset for tests
            f_tests = filter_tests(cov_map, test_mapping, TESTS_SUBSET_SIZE)
            # print(attacker.m_subset.mutants_ids)
            defender.t_subset = defender.new_subset(defender.t_suite.create_subset(f_tests, TESTS_SUBSET_SIZE))
            update_was_in_subset(defender.t_subset.tests_ids, defender)

            # Set up attacker and defender
            attacker.prepare_for_testing()

            # Find all tests covering mutants and create subsets for random and pick selection
            f_tests_cov = list()
            for m in attacker.m_subset.mutants_ids:
                for t in f_tests:
                    if int(m) in cov_map[test_mapping.index(t)] and t not in f_tests_cov:
                        f_tests_cov.append(t)
            while len(f_tests_cov) < MODEL_PICK_LIMIT_T:
                f_tests_cov.append(random.choice(f_tests_cov))
            f_tests_sub = f_tests_cov.copy()
            while len(f_tests_sub) > MODEL_PICK_LIMIT_T:
                f_tests_sub.remove(np.random.choice(f_tests_sub))

            defender.prepare_for_testing(f_tests_sub, f_tests_cov)

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
            print("Elapsed time for round %d: %.3f sec" % (x, elapsed_time))

            # Save to log file
            save_log_file(x, elapsed_time, gl_writer, log_line_dic)

    ''' End of The Game '''
    # Plot results
    plot_results(SHOW_PLOTS, True)

    # Produce mutants and tests files with information about them
    save_mutants_file()
    save_tests_file()

    # Save bandit models to a file
    if SAVE_BANDITS:
        defender.save_bandit(OUTPUT_RUN_DIR)
        attacker.save_bandit(OUTPUT_RUN_DIR)


def create_testing_files():
    """ Create testing folder with compiled src file using java 8 for compatibility reasons """
    p_path = '../generation/programs/' + PROGRAM
    t_path = p_path + '/testing/' + PROGRAM

    if not path.exists(t_path):
        makedirs(t_path)
        copyfile(p_path + '/src/' + SRC_FILE_NAME + '.java', t_path + '/' + SRC_FILE_NAME + '.java')
        run(['./' + 'compile_src_file_j8.sh', PROGRAM, SRC_FILE_NAME], cwd='../generation/')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=GAME_ITERATIONS)
    parser.add_argument('--mutants_subset_size', type=int, default=MUTANTS_SUBSET_SIZE)
    parser.add_argument('--tests_subset_size', type=int, default=TESTS_SUBSET_SIZE)
    parser.add_argument('--model_pick_limit_multiplier', type=float, default=MODEL_PICK_LIMIT_MULTIPLIER)
    parser.add_argument('--winning_threshold', type=float, default=WINNING_THRESHOLD)
    parser.add_argument('--attacker_mode', type=str, default=ATTACKER_MODE)
    parser.add_argument('--defender_mode', type=str, default=DEFENDER_MODE)
    parser.add_argument('--bandit_algorithm', type=str, default=BANDIT_ALGORITHM)
    parser.add_argument('--output_run_dir', type=str, default=OUTPUT_RUN_DIR)
    parser.add_argument('--program', type=str, default=PROGRAM)
    args = parser.parse_args()

    GAME_ITERATIONS = args.iterations
    MUTANTS_SUBSET_SIZE = args.mutants_subset_size
    TESTS_SUBSET_SIZE = args.tests_subset_size
    MODEL_PICK_LIMIT_MULTIPLIER = args.model_pick_limit_multiplier
    WINNING_THRESHOLD = args.winning_threshold
    ATTACKER_MODE = args.attacker_mode
    DEFENDER_MODE = args.defender_mode
    BANDIT_ALGORITHM = args.bandit_algorithm
    OUTPUT_RUN_DIR = args.output_run_dir + '_gis:%d_mss:%d_tss:%d_mplm:%.1f_wt:%.1f_am:%s_dm:%s_ba:%s' \
        % (GAME_ITERATIONS, MUTANTS_SUBSET_SIZE, TESTS_SUBSET_SIZE, MODEL_PICK_LIMIT_MULTIPLIER, WINNING_THRESHOLD,
           ATTACKER_MODE, DEFENDER_MODE, BANDIT_ALGORITHM)
    PROGRAM = args.program

    MODEL_PICK_LIMIT_M = math.ceil(MUTANTS_SUBSET_SIZE * MODEL_PICK_LIMIT_MULTIPLIER)
    MODEL_PICK_LIMIT_T = math.ceil(TESTS_SUBSET_SIZE * MODEL_PICK_LIMIT_MULTIPLIER)

    create_testing_files()

    # defender = Defender(DEFENDER_MODE, MODEL_PICK_LIMIT_T, TESTS_SUBSET_SIZE)
    # attacker = Attacker(ATTACKER_MODE, MODEL_PICK_LIMIT_M, MUTANTS_SUBSET_SIZE)
    # #
    # # # print(environ['PATH'])
    # #
    # main()
