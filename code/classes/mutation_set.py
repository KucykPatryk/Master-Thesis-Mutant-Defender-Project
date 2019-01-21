import random

from .global_variables import *


class MutationSet:
    def __init__(self, mutants):
        self.mutants_list = mutants  # A list of available mutants and their properties
        self.mutants_count = len(self.mutants_list)  # Number of mutants

    # Creates a subset with given mutant ids
    #
    # Parameters:
    #     ids_list: ids of the desired mutants as a list
    #
    # Returns:
    #     A new subset

    def create_subset(self, ids_list):
        subset = list()
        for i in range(SUBSET_SIZE):
            subset.append(self.mutants_list[ids_list[i]])
        return subset

    # Same as above, just random with n mutants
    def create_random_subset(self, n):
        subset = random.sample(self.mutants_list, n)
        return subset


class MutationSubset(MutationSet):
    def __init__(self, mutants_subset):
        super(MutationSubset, self).__init__(mutants_subset)

    # Produce a sorted list of mutant ids from the subset
    def return_mutant_ids(self):
        sorted_ids = list()
        for i in range(SUBSET_SIZE):
            sorted_ids.append(self.mutants_list[i].split(':')[0])
        sorted_ids.sort(key=int)
        return sorted_ids

    # Creates a file with only ids of the subset (eg. for the exculde mutants file)
    def create_n_mutant_ids_file(self):
        return
