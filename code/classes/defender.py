from subprocess import run

from .test_suite import TestSuite
from .test_suite import TestSubset

from .global_variables import *
from classes.vwwrapper import VWWrapper


class Defender:
    """ The Defender agent"""
    def __init__(self, mode):
        self.tests_ids = self.read_test_ids()
        self.t_suite = TestSuite(self.tests_ids, len(self.tests_ids))
        self.t_subset = self.new_subset(self.t_suite.create_random_subset(TESTS_SUBSET_SIZE))
        self.won = 0  # Times won against attacker
        self.lost = 0  # Times lost against attacker
        self.last_winner = False  # True if won in last round
        # Create the mutant Vowpal Wabbit model
        # self.vw_test = VWWrapper(
        #     '--quiet --cb_explore_adf --epsilon=0.1',
        #     '/home/kucyk-p/UiO/Master_Thesis/vowpal_wabbit/build/vowpalwabbit/vw')

        # This variable decides the agent mode. Currently "random" is supported
        self.agent_mode = mode
        self.features = ''

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
        self.last_winner = True

    def lose(self):
        """ Add a loss """
        self.lost += 1
        self.last_winner = False

    def update(self, won, killed, ids, kill_ratio):
        """ Update values after a round """
        if won:
            self.win()
        else:
            self.lose()

        self.t_subset.update_killed(killed)
        # self.t_subset.update_tests(ids, kill_ratio)
        self.t_suite.update_tests(ids, kill_ratio)

    def prepare_for_testing(self):
        """ Prepare agent for the execution """
        if self.agent_mode is 'bandit':
            # Test features
            # self.features =
            # print(self.features)

            # Prediction
            # TO BE IMPLEMENTED
            # Model selects the tests
            # m_pred =
            # print(m_pred)
            return

        elif self.agent_mode is 'random':
            # Select from the subsets based on MODEL_PICK_LIMIT parameter
            self.t_subset = TestSubset(self.t_subset.create_random_subset(MODEL_PICK_LIMIT), MODEL_PICK_LIMIT)

    def learn(self):
        """ Learn after the tests are run through Major and results are updated """
