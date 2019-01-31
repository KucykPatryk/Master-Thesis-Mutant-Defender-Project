from subprocess import run

from .mutation_set import MutationSet
from .mutation_set import MutationSubset

from .global_variables import *


class Attacker:
    def __init__(self):
        self.mutants_list = self.read_mutants()
        self.m_set = MutationSet(self.mutants_list, len(self.mutants_list))
        self.m_subset = MutationSubset(self.m_set.create_random_subset(), len(self.mutants_list))
        self.won = 0  # Times won against defender
        self.lost = 0  # Times lost against defender

    # Generates mutants with context and log files
    @staticmethod
    def generate_mutants():
        run(['./' + 'run_mutant_generation.sh'], cwd='../generation/')

    # Reads mutants from file and saves as a list
    @staticmethod
    def read_mutants():
        with open('../generation/mutants.log') as f:
            mutants_list = f.read().splitlines()

        return mutants_list

    # Add a win
    def win(self):
        self.won += 1

    # Add a loss
    def lose(self):
        self.lost += 1

    # Updates values after a round
    def update(self, won, summary, ids):
        if won:
            self.win()
        else:
            self.lose()

        self.m_subset.update_survived_killed(summary[3], summary[2])
        self.m_subset.update_mutants(won, ids)
