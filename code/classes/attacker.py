from subprocess import run
from .global_variables import *

from .mutation_set import MutationSet
from .mutation_set import MutationSubset
from sklearn.linear_model import LogisticRegression
from contextualbandits.online import BootstrappedUCB, BootstrappedTS, SeparateClassifiers, \
    EpsilonGreedy, AdaptiveGreedy, ExploreFirst, ActiveExplorer, SoftmaxExplorer
from copy import deepcopy
import numpy as np
import random

from sys import exit

import pandas as pd
from sklearn import preprocessing


class Attacker:
    """ The Attacker agent"""
    def __init__(self, mode, pick_limit, subset_size):
        self.mutants_list = self.read_mutants()
        self.m_set = MutationSet(self.mutants_list, len(self.mutants_list))
        self.m_subset = self.new_subset(self.m_set, subset_size)
        self.won = 0  # Times won against defender
        self.lost = 0  # Times lost against defender
        self.last_winner = False  # True if won in last round
        self.pick_limit = pick_limit
        self.encoder = object()

        # This variable decides the agent mode. Currently "random" is supported
        self.agent_mode = mode

    @staticmethod
    def generate_mutants():
        """ Generate mutants with context and log files """
        run(['./' + 'run_mutant_generation.sh'], cwd='../generation/')

    @staticmethod
    def read_mutants():
        """ Read mutants from file and saves as a list """
        with open('../generation/mutants.log') as f:
            mutants_list = f.read().splitlines()

        return mutants_list

    def new_subset(self, set, size):
        m_subset = MutationSubset(set.create_random_subset(size),
                                  len(self.mutants_list), size)
        return m_subset

    def new_selected_subset(self, set, size, ids):
        m_subset = MutationSubset(set.create_subset(ids, size),
                                  len(self.mutants_list), size)
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
    def features_encoder():
        """Encode mutant features with HotOneEncoder from mutant.context file

        :return: OneHotEncoder for mutant features
        """
        df = pd.read_csv('../generation/mutants.context', sep=',')
        cat1 = df.mutationOperatorGroup.unique()
        cat2 = df.mutationOperator.unique()
        cat3 = df.nodeTypeBasic.unique()
        cat4 = df.parentContextDetailed.unique()
        cat5 = df.parentStmtContextDetailed.unique()
        cat6 = df.hasVariableChild.unique()
        cat7 = df.hasOperatorChild.unique()
        cat8 = df.hasLiteralChild.unique()

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
        df = pd.read_csv('../generation/mutants.context', sep=',')
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
            algorithm = EpsilonGreedy(deepcopy(base_algorithm), nchoices=n_choices)

        return algorithm

    def prepare_for_testing(self):
        """ Prepare agent for the execution """
        if self.agent_mode is 'scikit':
            # Mutant features
            features = self.encode_features(self.m_subset.mutants_ids)

            # Prediction
            base_algorithm = LogisticRegression(random_state=123, solver='lbfgs')
            n_choises = 2
            algorithm = self.bandit_algorithm(BANDIT_ALGORITHM, base_algorithm, n_choises)

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

            # Model selects the mutants
            ids = np.random.choice(self.m_subset.mutants_ids, MODEL_PICK_LIMIT_M, p=pred.T[0], replace=False)
            # Creates the new subset

            print(self.m_subset.mutants_ids)
            self.m_subset = self.new_selected_subset(self.m_subset, self.pick_limit, ids.tolist())
            print(self.m_subset.mutants_ids)

        elif self.agent_mode is 'random':
            # Select from the subsets based on MODEL_PICK_LIMIT parameter
            self.m_subset = self.new_subset(self.m_subset, self.pick_limit)

    def learn(self):
        """ Learn after the tests are run through Major and results are updated """
