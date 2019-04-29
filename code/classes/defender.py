from subprocess import run
from os import path

from .test_suite import TestSuite
from .test_suite import TestSubset

from .global_variables import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from contextualbandits.online import BootstrappedUCB, BootstrappedTS, SeparateClassifiers, \
    EpsilonGreedy, AdaptiveGreedy, ExploreFirst, ActiveExplorer, SoftmaxExplorer
from copy import deepcopy
import dill


class Defender:
    """ The Defender agent"""
    def __init__(self, mode, pick_limit, subset_size):
        if not path.isdir('../generation/programs/' + PROGRAM + '/evosuite-tests'):
            self.generate_tests()
        self.tests_folder_name = next(walk('../generation/programs/' + PROGRAM + '/evosuite-tests/'))[1][0]
        self.tests_file_name = next(walk('../generation/programs/' + PROGRAM + '/evosuite-tests/' +
                                         self.tests_folder_name))[2][0]
        self.tests_ids = self.read_test_ids()
        self.t_suite = TestSuite(self.tests_ids, len(self.tests_ids))
        self.t_subset = self.new_subset(self.t_suite.create_random_subset(subset_size))
        self.won = 0  # Times won against attacker
        self.lost = 0  # Times lost against attacker
        self.last_winner = False  # True if won in last round
        self.pick_limit = pick_limit
        self.encoder = object()
        self.bandit = None

        # This variable decides the agent mode. Currently "random" is supported
        self.agent_mode = mode

    def create_bandit(self, num_features):
        """ Create and return a bandit algorithm object based on logistic regression
        :return: Bandit algorithm object
        """
        base_algorithm = SGDClassifier(random_state=123)
        n_choices = 2
        algorithm = self.bandit_algorithm(BANDIT_ALGORITHM, base_algorithm, n_choices)

        # Initial fit
        X = np.zeros((1, num_features))
        zeros = np.zeros(1)
        algorithm.fit(X, zeros, zeros)

        return algorithm

    def save_bandit(self):
        """ Save bandit to a binary file using dill """
        file = open('defender_bandit', 'wb')
        dill.dump(self.bandit, file)
        file.close()

    @staticmethod
    def generate_tests():
        """ Generate mutants with context and log files """
        run(['./' + 'run_tests_generation.sh', SRC_FOLDER_NAME, SRC_FILE_NAME, PROGRAM],
            cwd='../generation/')
        move_evosuite_files()

    def read_test_ids(self):
        """ Read test ids from the java file with tests and save it as a list """
        ids = list()
        with open('../generation/programs/' + PROGRAM + '/evosuite-tests/' + self.tests_folder_name + '/' +
                  self.tests_file_name) as f:
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
        self.t_suite.update_tests(ids, kill_ratio, self.t_subset.tests_ids)

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
            df = pd.read_csv('../generation/programs/' + PROGRAM + '/coverage_reports/coverage_report' +
                             nr, sep=',', dtype='category')
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
            algorithm = EpsilonGreedy(deepcopy(base_algorithm), nchoices=n_choices, batch_train=True)

        return algorithm

    def prepare_for_testing(self, f_tests_ids, f_tests_cov):
        """ Prepare agent for the execution """
        if self.agent_mode == 'scikit':
            features = self.encode_features(f_tests_cov)

            if not self.bandit:
                self.bandit = self.create_bandit(features.shape[1])

            # Prediction
            pred = self.bandit.decision_function(features)

            # Change pred values to prob, so they sum up to 1
            sum = np.sum(pred.T[0])
            pred.T[0] /= sum
            sum = np.sum(pred.T[1])
            pred.T[1] /= sum

            # Model selects the tests
            ids = np.random.choice(f_tests_cov, MODEL_PICK_LIMIT_T, p=pred.T[0], replace=False)

            # Create new subset
            self.t_subset = self.new_subset(self.t_subset.create_subset(ids, self.pick_limit))

        elif self.agent_mode == 'random':
            # Select from the subsets based on MODEL_PICK_LIMIT parameter
            self.t_subset = self.new_subset(self.t_subset.create_subset(f_tests_ids, self.pick_limit))

    def learn(self):
        """ Learn after the tests are run through Major and results are updated """
        features = self.encode_features(self.t_subset.tests_ids)
        a = np.zeros((features.shape[0]))
        rml = list()
        for t in self.t_subset.tests_ids:
            rml.append(1 if self.t_suite.tests[int(t) - 1].last_kill else 0)
        r = np.array(rml).reshape(len(rml))
        self.bandit.partial_fit(features, a, r)
