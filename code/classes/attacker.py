from subprocess import run
from os import path
import dill

from .global_variables import move_major_files, LOAD_BANDITS
from .mutation_set import MutationSet
from .mutation_set import MutationSubset
from sklearn.linear_model import SGDClassifier, LogisticRegression
from contextualbandits.online import BootstrappedUCB, BootstrappedTS, SeparateClassifiers, \
    EpsilonGreedy, AdaptiveGreedy, ExploreFirst, ActiveExplorer, SoftmaxExplorer
from copy import deepcopy
import numpy as np

import pandas as pd
from sklearn import preprocessing


class Attacker:
    """ The Attacker agent"""
    def __init__(self, mode, pick_limit, subset_size, program):
        self.program = program  # String of program name
        if not path.isdir('../generation/programs/' + program + '/mutants'):
            self.generate_mutants()
        self.mutants_list = self.read_mutants(program)
        self.mutants_len = len(self.mutants_list)
        self.m_set = MutationSet(self.mutants_list, len(self.mutants_list), program)
        self.m_subset = self.new_subset(self.m_set, subset_size)
        self.won = 0  # Times won against defender
        self.lost = 0  # Times lost against defender
        self.last_winner = False  # True if won in last round
        self.pick_limit = pick_limit
        self.encoder = object()
        self.bandit = None

        # This variable decides the agent mode. Currently "random" is supported
        self.agent_mode = mode

    def create_bandit(self, num_features, bandit_algorithm):
        """ Create and return a bandit algorithm object based on logistic regression
        :return: Bandit algorithm object
        """
        if bandit_algorithm == 'ActiveExplorer':
            base_algorithm = SGDClassifier(random_state=123, loss='log')
        else:
            base_algorithm = SGDClassifier(random_state=123)
        n_choices = 2
        algorithm = self.bandit_algorithm(bandit_algorithm, base_algorithm, n_choices)
        # Initial fit
        X = np.zeros((1, num_features))
        zeros = np.zeros(1)
        algorithm.fit(X, zeros, zeros)

        return algorithm

    def save_bandit(self, folder_run_name, based_on, load_bandits):
        """ Save bandit to a binary file using dill
        :param folder_run_name: Folder name in which it is saved
        :param based_on: dir to the loaded bandit for this run
        :return:
        """
        file = open('output/' + self.program + '/' + folder_run_name + '/attacker_bandit', 'wb')
        dill.dump(self.bandit, file)
        file.close()
        #  Write to log file the last loaded bandit file
        if not load_bandits:
            based_on = 'none'
            with open('output/' + self.program + '/' + folder_run_name + '/loaded_bandits', 'w') as lb:
                lb.write(based_on + '-ATTACKER\n')
        with open('output/' + self.program + '/' + folder_run_name + '/loaded_bandits', 'a') as lb:
            lb.write(based_on + '-ATTACKER\n')

    def load_bandit(self, b_dir):
        """ Load bandit from a binary file using dill """
        file = open('output/' + b_dir + '/attacker_bandit', 'rb')
        self.bandit = dill.load(file)
        file.close()

    def generate_mutants(self):
        """ Generate mutants with context and log files """
        run(['./' + 'run_mutant_generation.sh', self.program], cwd='../generation/')
        move_major_files(self.program)

    @staticmethod
    def read_mutants(program):
        """ Read mutants from file and saves as a list """
        with open('../generation/programs/' + program + '/mutants.log') as f:
            mutants_list = f.read().splitlines()

        return mutants_list

    def new_subset(self, set, size):
        m_subset = MutationSubset(set.create_random_subset(size),
                                  len(self.mutants_list), size, self.program)
        return m_subset

    def new_selected_subset(self, set, size, ids):
        m_subset = MutationSubset(set.create_subset(ids, size),
                                  len(self.mutants_list), size, self.program)
        return m_subset

    def win(self):
        """ Add a win """
        self.won += 1
        self.last_winner = True

    def lose(self):
        """ Add a loss """
        self.lost += 1
        self.last_winner = False

    def update(self, won, summary, ids, kill_ratio):
        """ Update values after a round """
        if won:
            self.win()
        else:
            self.lose()

        self.m_subset.update_survived_killed(summary[3], summary[2])
        self.m_set.update_mutants(ids, kill_ratio, self.m_subset.mutants_ids)

    def update_wis(self, subset_ids):
        """ Update was in subset count """
        self.m_set.update_wis(subset_ids)

    @staticmethod
    def features_encoder(program):
        """Encode mutant features with HotOneEncoder from mutant.context file

        :return: OneHotEncoder for mutant features
        """
        cats = []
        df = pd.read_csv('../generation/programs/' + program + '/mutants.context', sep=',')
        cat1 = df.mutationOperatorGroup.unique()
        cat2 = df.mutationOperator.unique()
        cat3 = df.nodeTypeBasic.unique()
        cat3 = [x for x in cat3 if str(x) != 'nan']
        cat3 = np.asarray(cat3)
        cat4 = df.parentContextDetailed.unique()
        cat5 = df.parentStmtContextDetailed.unique()
        cat6 = df.hasVariableChild.unique()
        cat7 = df.hasOperatorChild.unique()
        cat8 = df.hasLiteralChild.unique()

        extra = np.array(range(1, 50 - len(cat1)))
        cat1 = np.hstack([cat1, extra])
        extra = np.array(range(1, 50 - len(cat2)))
        cat2 = np.hstack([cat2, extra])
        extra = np.array(range(1, 50 - len(cat3)))
        cat3 = np.hstack([cat3, extra])
        extra = np.array(range(1, 50 - len(cat4)))
        cat4 = np.hstack([cat4, extra])
        extra = np.array(range(1, 50 - len(cat5)))
        cat5 = np.hstack([cat5, extra])
        if len(cat6) < 2:
            cat6 = np.array([0, 1])
        if len(cat7) < 2:
            cat7 = np.array([0, 1])
        if len(cat8) < 2:
            cat8 = np.array([0, 1])

        enc = preprocessing.OneHotEncoder(handle_unknown='ignore',
                                          categories=[cat1, cat2, cat3, cat4, cat5, cat6, cat7, cat8])

        x = [[cat1[0], cat2[0], cat3[0], cat4[0], cat5[0], cat6[0], cat7[0], cat8[0]],
             [cat1[-1], cat2[-1], cat3[-1], cat4[-1], cat5[-1], cat6[-1], cat7[-1], cat8[-1]]]

        enc.fit(x)
        return enc

    def encode_features(self, mutant_nrs):
        """ Return encoded features

        :param mutant_nrs: list of mutant ids to transform into features
        :return: a feature vector
        """
        df = pd.read_csv('../generation/programs/' + self.program + '/mutants.context', sep=',')
        df = df.fillna(0)
        feature_list = list()
        features = list()
        for m in mutant_nrs:
            feature_list.append(df.mutationOperatorGroup[int(m) - 1])
            feature_list.append(df.mutationOperator[int(m) - 1])
            feature_list.append(df.nodeTypeBasic[int(m) - 1])
            feature_list.append(df.parentContextDetailed[int(m) - 1])
            feature_list.append(df.parentStmtContextDetailed[int(m) - 1])
            feature_list.append(df.hasVariableChild[int(m) - 1])
            feature_list.append(df.hasOperatorChild[int(m) - 1])
            feature_list.append(df.hasLiteralChild[int(m) - 1])
            features.append(feature_list.copy())
            feature_list.clear()

        # encoded_features = self.encoder.transform(np.where(features == 'nan', 'null', features)).toarray()
        encoded_features = self.encoder.transform(features).toarray()
        return encoded_features

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
        elif algorithm_name == 'AdaptiveGreedy':
            algorithm = AdaptiveGreedy(deepcopy(base_algorithm), nchoices=n_choices, batch_train=True)
        elif algorithm_name == 'ActiveExplorer':
            algorithm = ActiveExplorer(deepcopy(base_algorithm), nchoices=n_choices, batch_train=True)
        elif algorithm_name == 'SoftmaxExplorer':
            algorithm = SoftmaxExplorer(deepcopy(base_algorithm), nchoices=n_choices, batch_train=True)

        return algorithm

    def prepare_for_testing(self, model_pick_limit_m, bandit_algorithm):
        """ Prepare agent for the execution """
        if self.agent_mode == 'scikit':
            # Mutant features
            features = self.encode_features(self.m_subset.mutants_ids)

            if not self.bandit:
                self.bandit = self.create_bandit(features.shape[1], bandit_algorithm)

            # Prediction
            pred = self.bandit.decision_function(features)

            # Change pred values to prob, so they sum up to 1
            sum = np.sum(pred.T[0])
            pred.T[0] /= sum
            sum = np.sum(pred.T[1])
            pred.T[1] /= sum

            # Model selects the mutants
            ids = np.random.choice(self.m_subset.mutants_ids, model_pick_limit_m, p=pred.T[0], replace=False)

            # Create new subset
            self.m_subset = self.new_selected_subset(self.m_subset, self.pick_limit, ids.tolist())

        elif self.agent_mode == 'random':
            # Select from the subsets based on MODEL_PICK_LIMIT parameter
            self.m_subset = self.new_subset(self.m_subset, self.pick_limit)

    def learn(self):
        """ Learn after the tests are run through Major and results are updated """
        features = self.encode_features(self.m_subset.mutants_ids)
        a = np.zeros((features.shape[0]))
        rml = list()
        for m in self.m_subset.mutants_ids:
            rml.append(1 if self.m_set.mutants[int(m)-1].last_killed else 0)
        r = np.array(rml).reshape(len(rml))
        self.bandit.partial_fit(features, a, r)
