from subprocess import run

from .mutation_set import MutationSet
from .mutation_set import MutationSubset

from csv import DictReader
import pandas as pd
from sklearn import preprocessing
import sys

from classes.vwwrapper import VWWrapper


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
        self.features = ''

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
    def encode_features():
        """ Encode mutant features with HotOneEncoder from mutant.context file """
        df = pd.read_csv('../generation/mutants.context', sep=',', dtype='category')
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

        print(enc.fit(x))
        return enc

    def prepare_for_testing(self):
        """ Prepare agent for the execution """
        if self.agent_mode is 'scikit':
            # Mutant features
            # self.features = self.encoder.transform([[]].toarray())
            # print(self.features)

            # Prediction
            # TO BE IMPLEMENTED
            # Model selects the mutants
            # m_pred = attacker.vw_mutant.predict(mutants_features)
            # print(m_pred)

        elif self.agent_mode is 'random':
            # Select from the subsets based on MODEL_PICK_LIMIT parameter
            self.m_subset = self.new_subset(self.m_subset, self.pick_limit)

    def learn(self):
        """ Learn after the tests are run through Major and results are updated """