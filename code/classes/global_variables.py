from os import walk
import math

GAME_ITERATIONS = 5

MUTANTS_SUBSET_SIZE = 15
TESTS_SUBSET_SIZE = 15
MODEL_PICK_LIMIT = math.ceil(MUTANTS_SUBSET_SIZE * 0.3)

TESTS_FOLDER_NAME = next(walk('../generation/evosuite-tests/'))[1][0]
TESTS_FILE_NAME = next(walk('../generation/evosuite-tests/' + TESTS_FOLDER_NAME))[2][0]

WINNING_THRESHOLD = 0.5  # Percentage for winning by killing mutants

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
