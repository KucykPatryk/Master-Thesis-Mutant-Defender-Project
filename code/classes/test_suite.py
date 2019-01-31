import random

from .test import Test

from .global_variables import *


# Class representing the whole testing suite

class TestSuite:
    def __init__(self, tests, count):
        self.tests_ids = tests  # A list of available tests as their names
        self.tests_count = count  # Number of all tests
        self.tests = list()  # All tests where the id is equal to index

        # Fill up the lists with unique tests
        for t in range(self.tests_count):
            self.tests.append(Test(t, 0))

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

class TestSubset(TestSuite):
    def __init__(self, subset_ids, count):
        super(TestSubset, self).__init__(subset_ids, count)
        self.killed = 0  # How many mutants were killed in the opposed subset

    # Update the killed value
    def update_killed(self, value):
        self.killed = value

    # Update test values
    #
    # Parameters:
    #     won: True if won or False if lost
    #     ids: a list with test ids that killed
    #
    # Returns:
    #     nothing

    def update_tests(self, ids, kill_ratio):
        for i in range(len(ids)):
            self.tests[int(ids[i])].update_kills()
        for x in self.tests_ids:
            x_id = int(x[4:])
            if x_id not in ids:
                self.tests[x_id].update_score(kill_ratio)
