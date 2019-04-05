import random

from .mutant import Mutant

from .global_variables import *


class MutationSet:
    """ Class representing the whole mutation set """
    def __init__(self, mutants, count):
        self.mutants_list = mutants  # A list of available mutants and their properties
        self.mutants_ids = [x[:x.index(':')] for x in self.mutants_list]
        self.mutants_count = count  # Number of all mutants
        self.mutants = list()  # All mutants where the id is index + 1

        # Fill up the lists with unique mutants
        for m in range(self.mutants_count):
            self.mutants.append(Mutant(m + 1, 0))

    def create_subset(self, ids_list, size):
        """ Create a subset with given mutant ids
        :param ids_list: ids of the desired mutants as a list
        :return: a new subset
        """
        subset = list()
        for i in range(size):
            subset.append(self.mutants_list[self.mutants_ids.index(ids_list[i])])
        return subset

    def create_random_subset(self, size):
        """ Same as above, just random with n mutants """
        subset = random.sample(self.mutants_list, size)
        return subset

    def update_mutants(self, ids, kill_ratio, subset_ids):
        """ Update mutant values

        :param ids: a list with mutant ids that were killed
        :param kill_ratio: kill ratio
        :param subset_ids: ids of the last subset
        :return: nothing
        """
        # Updated killed mutants
        for i in range(len(ids)):
            self.mutants[int(ids[i]) - 1].update_kills()
            self.mutants[int(ids[i]) - 1].update_score(-(1 + kill_ratio))
        # Update survived mutants
        for x in subset_ids:
            self.mutants[int(x) - 1].update_selected()
            if str(x) not in ids:
                self.mutants[int(x) - 1].update_score(1 + kill_ratio)
                self.mutants[int(x) - 1].update_survived()

    def update_wis(self, subset_ids):
        """ Update was in subset count """
        for x in subset_ids:
            self.mutants[int(x) - 1].update_subset_chosen()


class MutationSubset(MutationSet):
    """ Class representing the created subset """
    def __init__(self, mutants_subset, count, size):
        super(MutationSubset, self).__init__(mutants_subset, count)
        self.excluded_sorted_ids = self.excluded_mutant_ids(size)
        self.create_exclude_ids_file()
        self.survived = 0  # How many mutants survived
        self.killed = 0  # How many were killed

    def excluded_mutant_ids(self, size):
        """ Produce a sorted list of mutant ids not from the subset """
        sorted_ids = list(range(1, self.mutants_count + 1))
        subset_ids = list()

        for i in range(size):
            subset_ids.append(int(self.mutants_list[i].split(':')[0]))

        sorted_ids = [e for e in sorted_ids if e not in subset_ids]
        # sorted_ids.sort(key=int)
        return sorted_ids

    def create_exclude_ids_file(self):
        """ Create a file with only ids of the not in the subset (eg. for the exclude mutants file) """
        with open('../generation/exclude_mutants.txt', 'w') as ef:
            ef.writelines('%s\n' % l for l in self.excluded_sorted_ids)

    def update_survived_killed(self, s, k):
        """ Update the survived/killed value """
        self.survived = s
        self.killed = k
