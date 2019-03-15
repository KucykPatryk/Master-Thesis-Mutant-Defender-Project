from subprocess import run

from .mutation_set import MutationSet
from .mutation_set import MutationSubset

from .global_variables import *
from classes.vwwrapper import VWWrapper


class Attacker:
    """ The Attacker agent"""
    def __init__(self):
        self.mutants_list = self.read_mutants()
        self.m_set = MutationSet(self.mutants_list, len(self.mutants_list))
        self.m_subset = self.new_subset()
        self.won = 0  # Times won against defender
        self.lost = 0  # Times lost against defender
        # Create the mutant Vowpal Wabbit model
        self.vw_mutant = VWWrapper(
            '--quiet --cb_explore_adf --epsilon=0.1',
            '/home/kucyk-p/UiO/Master_Thesis/vowpal_wabbit/build/vowpalwabbit/vw')

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

    def new_subset(self):
        m_subset = MutationSubset(self.m_set.create_random_subset(), len(self.mutants_list))
        return m_subset

    def win(self):
        """ Add a win """
        self.won += 1

    def lose(self):
        """ Add a loss """
        self.lost += 1

    def update(self, won, summary, ids, kill_ratio):
        """ Update values after a round """
        if won:
            self.win()
        else:
            self.lose()

        self.m_subset.update_survived_killed(summary[3], summary[2])
        self.m_set.update_mutants(ids, kill_ratio, self.m_subset.mutants_ids)
