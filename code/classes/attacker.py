from subprocess import run

from .mutation_set import MutationSet
from .mutation_set import MutationSubset

from .global_variables import *


class Attacker:
    def __init__(self):
        self.mutants_list = self.read_mutants()
        self.m_set = MutationSet(self.mutants_list, len(self.mutants_list))
        self.m_subset = MutationSubset(self.m_set.create_random_subset(SUBSET_SIZE), len(self.mutants_list))

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
