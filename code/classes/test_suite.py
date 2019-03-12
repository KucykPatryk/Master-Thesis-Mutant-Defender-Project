import random

from .test import Test

from .global_variables import *


class TestSuite:
    """ Class representing the whole testing suite """
    def __init__(self, tests, count):
        self.tests_ids = tests  # A list of available tests as their name ids
        self.tests_count = count  # Number of all tests
        self.tests = list()  # All tests where the id is equal to index

        # Fill up the lists with unique tests
        for t in range(self.tests_count):
            self.tests.append(Test(t + 1, 0))

    def create_subset(self, ids_list):
        """ Create a subset with given test ids

        :param ids_list: ids of the desired tests as a list
        :return: a new subset
        """
        subset = list()
        for i in range(TESTS_SUBSET_SIZE):
            subset.append(self.tests_ids[int(ids_list[i])])
        return subset

    def create_random_subset(self):
        """ Same as above, just random """
        subset = random.sample(self.tests_ids, TESTS_SUBSET_SIZE)
        return subset


class TestSubset(TestSuite):
    """ Class representing the created subset """
    def __init__(self, subset_ids, count):
        super(TestSubset, self).__init__(subset_ids, count)
        self.killed = 0  # How many mutants were killed in the opposed subset

    def update_killed(self, value):
        """ Update the killed value """
        self.killed = value

    def update_tests(self, ids, kill_ratio):
        """ Update test values

        :param ids: a list with test ids that killed
        :param kill_ratio: kill ratio
        :return: nothing
        """
        test_map = test_map_array()
        for i in range(len(ids)):
            self.tests[test_map[int(ids[i])]].update_kills()
            self.tests[test_map[int(ids[i])]].update_score(kill_ratio)
        # for x in self.tests_ids:
        #     x_id = int(x[4:])
        #     if str(x_id) not in ids:
        #         self.tests[x_id].update_score(kill_ratio)
