from subprocess import run

from .test_suite import TestSuite
from .test_suite import TestSubset

from .global_variables import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from contextualbandits.online import BootstrappedUCB, BootstrappedTS, SeparateClassifiers, \
    EpsilonGreedy, AdaptiveGreedy, ExploreFirst, ActiveExplorer, SoftmaxExplorer
from copy import deepcopy


class Defender:
    """ The Defender agent"""
    def __init__(self, mode, pick_limit, subset_size):
        self.tests_ids = self.read_test_ids()
        self.t_suite = TestSuite(self.tests_ids, len(self.tests_ids))
        self.t_subset = self.new_subset(self.t_suite.create_random_subset(subset_size))
        self.won = 0  # Times won against attacker
        self.lost = 0  # Times lost against attacker
        self.last_winner = False  # True if won in last round
        self.pick_limit = pick_limit
        self.encoder = object()

        # This variable decides the agent mode. Currently "random" is supported
        self.agent_mode = mode

    @staticmethod
    def generate_tests():
        """ Generate mutants with context and log files """
        run(['./' + 'run_tests_generation.sh', SRC_FOLDER_NAME, SRC_FILE_NAME], cwd='../generation/')

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

    def update_wis(self, subset_ids):
        """ Update was in subset count """
        self.t_suite.update_wis(subset_ids)

    def encode_features(self, test_nrs):
        """ Encode test features

        :param test_nrs: list of test to make feature vector from
        :return: scaled feature vector as an array
        """
        # Retrieve coverage information from the report files
        v = list()
        a = np.empty([0, 12], dtype=np.float64)
        for nr in test_nrs:
            df = pd.read_csv('../generation/coverage_reports/coverage_report' + nr, sep=',', dtype='category')
            for e in df.columns[3:]:
                v.append(float(df[e][0]))
            v.append((float(self.t_suite.tests[int(nr)].killed_times)))
            v.append((float(self.t_suite.tests[int(nr)].selected)))
            a = np.append(a, [v], axis=0)
            v.clear()

        # Scale values
        scaler = StandardScaler()
        scaler.fit(a)

        return scaler.transform(a)

    @staticmethod
    def bandit_algorithm(algorithm_name, base_algorithm, n_choices):
        """
        Returns the given by parameter BANDIT_ALGORITHM algorithm
        :param algorithm_name: Name of the algorithm
        :param base_algorithm: logistic regression
        :param n_choices: n choices
        :return: the algorithm
        """
        algorithm = object()
        if algorithm_name == 'EpsilonGreedy':
            algorithm = EpsilonGreedy(deepcopy(base_algorithm), nchoices=n_choices)

        return algorithm

    def prepare_for_testing(self, f_tests_ids, f_tests_cov):
        """ Prepare agent for the execution """
        if self.agent_mode is 'scikit':
            features = self.encode_features(f_tests_cov)

            # Prediction
            base_algorithm = LogisticRegression(random_state=123, solver='lbfgs')
            n_choices = 2
            algorithm = self.bandit_algorithm(BANDIT_ALGORITHM, base_algorithm, n_choices)

            # Initial fit
            X = np.zeros((1, features.shape[1]))
            zeros = np.zeros(1)
            algorithm.partial_fit(X, zeros, zeros)

            pred = algorithm.decision_function(features)

            # Change pred values to prob, so they sum up to 1
            sum = np.sum(pred.T[0])
            pred.T[0] /= sum
            sum = np.sum(pred.T[1])
            pred.T[1] /= sum

            # Model selects the tests
            ids = np.random.choice(f_tests_cov, MODEL_PICK_LIMIT_T, p=pred.T[0], replace=False)

            # Create new subset
            self.t_subset = self.new_subset(self.t_subset.create_subset(ids, self.pick_limit))

        elif self.agent_mode is 'random':
            # Select from the subsets based on MODEL_PICK_LIMIT parameter
            self.t_subset = self.new_subset(self.t_subset.create_subset(f_tests_ids, self.pick_limit))

    def learn(self):
        """ Learn after the tests are run through Major and results are updated """
