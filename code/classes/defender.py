from subprocess import run

from .test_suite import TestSuite
from .test_suite import TestSubset

from .global_variables import *


class Defender:
    def __init__(self):
        self.tests_ids = self.read_test_ids()
        self.t_suite = TestSuite(self.tests_ids, len(self.tests_ids))
        self.t_subset = TestSubset(self.t_suite.create_random_subset(), len(self.tests_ids))
        self.won = 0  # Times won against attacker
        self.lost = 0  # Times lost against attacker

    # Generates mutants with context and log files
    @staticmethod
    def generate_tests():
        run(['./' + 'run_tests_generation.sh'], cwd='../generation/')

    # Reads test ids from the java file with tests and save it as a list
    @staticmethod
    def read_test_ids():
        ids = list()
        with open('../generation/evosuite-tests/' + TESTS_FOLDER_NAME + '/' + TESTS_FILE_NAME) as f:
            for line in f:
                if line[:13] in '  public void':
                    ln = line.split()
                    tn = ln[2].split('(')[0]
                    ids.append(tn)
        return ids

    # Add a win
    def win(self):
        self.won += 1

    # Add a loss
    def lose(self):
        self.lost += 1

    # Updates values after a round
    def update(self, won, killed, ids):
        if won:
            self.win()
        else:
            self.lose()

        self.t_subset.update_killed(killed)
        self.t_subset.update_tests(won, ids)
