from os import walk
import math


GAME_ITERATIONS = 1

MUTANTS_SUBSET_SIZE = 15
TESTS_SUBSET_SIZE = 15
MODEL_PICK_LIMIT_MULTIPLIER = 0.3
MODEL_PICK_LIMIT_M = math.ceil(MUTANTS_SUBSET_SIZE * MODEL_PICK_LIMIT_MULTIPLIER)
MODEL_PICK_LIMIT_T = math.ceil(TESTS_SUBSET_SIZE * MODEL_PICK_LIMIT_MULTIPLIER)
WINNING_THRESHOLD = 0.5  # Percentage for winning by killing mutants
OUTPUT_RUN_DIR = 'run0'
ATTACKER_MODE = 'scikit'
DEFENDER_MODE = 'random'

SHOW_PLOTS = False

TESTS_FOLDER_NAME = next(walk('../generation/evosuite-tests/'))[1][0]
TESTS_FILE_NAME = next(walk('../generation/evosuite-tests/' + TESTS_FOLDER_NAME))[2][0]

SRC_FILE_NAME = TESTS_FOLDER_NAME.capitalize()  # Name without he extension
SRC_FOLDER_NAME = TESTS_FOLDER_NAME



# with open('../generation/summary.csv') as f:
#     f.readline()
#     MUTANTS_COUNT = int(f.readline().split(',')[0])  # Number of all mutants
#
# with open('../generation/testMap.csv') as f2:
#     lines = f2.read().splitlines()
#     last_line = lines[-1]
#     TEST_COUNT = int(last_line.split(',')[0])  # Number of all tests


def test_map_array(file_path='../generation/testMap.csv'):
    """ Returns an array of test ids with their actual method ids
    Array ID is TestNo and Array value is TestName number """
    tests = [0]

    with open(file_path) as tm:
        tm.readline()
        for line in tm:
            line = line.split(',')
            tests.append(line[1][29:-2])

    return tests
