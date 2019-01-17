from subprocess import run

from .mutation_set import MutationSet


class Attacker:
    def __init__(self):
        self.m_set = MutationSet(self.read_mutants())

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
