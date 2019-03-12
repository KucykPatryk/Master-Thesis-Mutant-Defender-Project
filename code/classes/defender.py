from subprocess import run

from .test_suite import TestSuite
from .test_suite import TestSubset

from .global_variables import *
from classes.vwwrapper import VWWrapper


class Defender:
    """ The Defender agent"""
    def __init__(self):
        self.tests_ids = self.read_test_ids()
        self.t_suite = TestSuite(self.tests_ids, len(self.tests_ids))
        self.t_subset = self.new_subset(self.t_suite.create_random_subset())
        self.won = 0  # Times won against attacker
        self.lost = 0  # Times lost against attacker
        # Create the mutant Vowpal Wabbit model
        # self.vw_test = VWWrapper('--quiet --cb_explore_adf --epsilon=0.1',
        #                       '/home/kucyk-p/UiO/Master_Thesis/vowpal_wabbit/build/vowpalwabbit/vw')

    @staticmethod
    def generate_tests():
        """ Generate mutants with context and log files """
        run(['./' + 'run_tests_generation.sh'], cwd='../generation/')

    @staticmethod
    def read_test_ids():
        """ Read test ids from the java file with tests and save it as a list """
        ids = list()
        with open('../generation/evosuite-tests/' + TESTS_FOLDER_NAME + '/' + TESTS_FILE_NAME) as f:
            for line in f:
                if line[:13] in '  public void':
                    ln = line.split()
                    tn = ln[2].split('(')[0][4:]
                    ids.append(tn)
        return ids

    def new_subset(self, create_method):
        t_subset = TestSubset(create_method, len(self.tests_ids))
        return t_subset

    def win(self):
        """ Add a win """
        self.won += 1

    def lose(self):
        """ Add a loss """
        self.lost += 1

    def update(self, won, killed, ids, kill_ratio):
        """ Update values after a round """
        if won:
            self.win()
        else:
            self.lose()

        self.t_subset.update_killed(killed)
        self.t_subset.update_tests(ids, kill_ratio)
