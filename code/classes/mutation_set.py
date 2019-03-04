import random

from .mutant import Mutant

from .global_variables import *


# Class representing the whole mutation set

class MutationSet:
    def __init__(self, mutants, count):
        self.mutants_list = mutants  # A list of available mutants and their properties
        self.mutants_count = count  # Number of all mutants
        self.mutants = list()  # All mutants where the id is index + 1

        # Fill up the lists with unique mutants
        for m in range(self.mutants_count):
            self.mutants.append(Mutant(m + 1, 0))

    # Creates a subset with given mutant ids
    #
    # Parameters:
    #     ids_list: ids of the desired mutants as a list
    #
    # Returns:
    #     A new subset

    def create_subset(self, ids_list):
        subset = list()
        for i in range(MUTANTS_SUBSET_SIZE):
            subset.append(self.mutants_list[ids_list[i] - 1])
        return subset

    # Same as above, just random with n mutants
    def create_random_subset(self):
        subset = random.sample(self.mutants_list, MUTANTS_SUBSET_SIZE)
        return subset


# Class representing the created subset

class MutationSubset(MutationSet):
    def __init__(self, mutants_subset, count):
        super(MutationSubset, self).__init__(mutants_subset, count)
        self.excluded_sorted_ids = self.excluded_mutant_ids()
        self.create_exclude_ids_file()
        self.survived = 0  # How many mutants survived
        self.killed = 0  # How many were killed

    # Produce a sorted list of mutant ids not from the subset
    def excluded_mutant_ids(self):
        sorted_ids = list(range(1, self.mutants_count + 1))
        subset_ids = list()

        for i in range(MUTANTS_SUBSET_SIZE):
            subset_ids.append(int(self.mutants_list[i].split(':')[0]))

        sorted_ids = [e for e in sorted_ids if e not in subset_ids]
        # sorted_ids.sort(key=int)
        return sorted_ids

    # Creates a file with only ids of the not in the subset (eg. for the exclude mutants file)
    def create_exclude_ids_file(self):
        with open('../generation/exclude_mutants.txt', 'w+') as ef:
            ef.writelines('%s\n' % l for l in self.excluded_sorted_ids)

    # Update the survived/killed value
    def update_survived_killed(self, s, k):
        self.survived = s
        self.killed = k

    # Update mutant values
    #
    # Parameters:
    #     won: True if won or False if lost
    #     ids: a list with mutant ids that were killed
    #
    # Returns:
    #     nothing

    def update_mutants(self, ids, kill_ratio):
        # Updated killed mutants
        for i in range(len(ids)):
            self.mutants[int(ids[i])].update_kills()
            self.mutants[int(ids[i])].update_score(-kill_ratio)
        # Update survived mutants
        for x in self.mutants_list:
            x_id = int(x.split(':')[0])
            if str(x_id) not in ids:
                self.mutants[x_id].update_score(kill_ratio)
