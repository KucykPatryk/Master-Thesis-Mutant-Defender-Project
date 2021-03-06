from os import walk, path
import math
import shutil

GAME_ITERATIONS = 5

MUTANTS_SUBSET_SIZE = 10  # Initial size values
TESTS_SUBSET_SIZE = 25
MODEL_PICK_LIMIT_MULTIPLIER = 0.3
MODEL_PICK_LIMIT_M = math.ceil(MUTANTS_SUBSET_SIZE * MODEL_PICK_LIMIT_MULTIPLIER)
MODEL_PICK_LIMIT_T = math.ceil(TESTS_SUBSET_SIZE * MODEL_PICK_LIMIT_MULTIPLIER)
WINNING_THRESHOLD = 0.25  # Percentage for winning by killing mutants
ATTACKER_MODE = 'scikit'  # random or scikit
DEFENDER_MODE = 'scikit'  # random or scikit
BANDIT_ALGORITHM = 'EpsilonGreedy'
OUTPUT_RUN_DIR = 'run0'
PROGRAM = 'fontinfo'
SAVE_BANDITS = True
LOAD_BANDITS = False

SHOW_PLOTS = False

SRC_FILE_NAME = next(walk('../generation/programs/' + PROGRAM + '/src/'))[2][0][:-5]  # Name without the extension
SRC_FOLDER_NAME = SRC_FILE_NAME.lower()


def test_map_array(file_path='../generation/programs/' + PROGRAM + '/testMap-' + PROGRAM + '.csv'):
    """ Returns an array of test ids with their actual method ids
    Array ID is TestNo and Array value is TestName number """
    tests = [0]

    with open(file_path) as tm:
        tm.readline()
        for line in tm:
            line = line.split(',')
            tests.append(line[1][-4:-2])

    return tests


def move_major_files(program):
    shutil.move(path.join("../generation/", "mutants.log"),
                path.join("../generation/programs/" + program + "/", "mutants.log"))
    shutil.move(path.join("../generation/", "mutants.context"),
                path.join("../generation/programs/" + program + "/", "mutants.context"))
    shutil.move(path.join("../generation/mutants"),
                path.join("../generation/programs/" + program + "/"))


def move_evosuite_files(program):
    shutil.move("../generation/evosuite-tests", "../generation/programs/" + program + "/")
    shutil.move("../generation/evosuite-report", "../generation/programs/" + program + "/")
