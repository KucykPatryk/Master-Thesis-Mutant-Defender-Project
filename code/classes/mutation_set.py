import random


SUBSET_SIZE = 5

class MutationSet:
    def __init__(self, mutants):
        self.mutants_list = mutants  # A list of available mutants and their properties
        self.mutants_count = len(self.mutants_list)  # Number of mutants
        self.subset = self.create_random_subset(SUBSET_SIZE)

    # Creates a subset with a given mutant ids
    #
    # Parameters:
    #     ids_list: ids of the desired mutants as a list
    #
    # Returns:
    #     A new subset

    def create_subset(self, ids_list):
        for i in range(SUBSET_SIZE):
            subset = self.mutants_list[ids_list[i]]
        return subset

    # Same as above, just random with n mutants
    def create_random_subset(self, n):
        subset = random.sample(self.mutants_list, n)
        subset.sort()
        return subset


class MutationSubset(MutationSet):
    def __init__(self, mutants_subset):
        MutationSet.__init__(mutants_subset)

    # Produce a sorted list of mutant ids from the subset
    def return_mutant_ids(self, n):
        return

    # Creates a file with only ids of the subset (eg. for the exculde mutants file)
    def create_n_mutant_ids_file(self):
        return
