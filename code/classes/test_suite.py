import random

from .global_variables import *


# Class representing the whole testing suite

class TestSuite:
    def __init__(self, tests, count):
        self.tests_ids = tests  # A list of available tests as their names
        self.tests_count = count  # Number of all tests

    # Creates a subset with given test ids
    #
    # Parameters:
    #     ids_list: ids of the desired tests as a list
    #
    # Returns:
    #     A new subset

    def create_subset(self, ids_list):
        subset = list()
        for i in range(TESTS_SUBSET_SIZE):
            subset.append(self.tests_ids[ids_list[i]])
        return subset

    # Same as above, just random
    def create_random_subset(self):
        subset = random.sample(self.tests_ids, TESTS_SUBSET_SIZE)
        return subset


# Class representing the created subset

class TestSubset:
    def __init__(self):
        return