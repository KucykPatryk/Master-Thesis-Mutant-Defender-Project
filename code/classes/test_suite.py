import random

from .test import Test

from .global_variables import test_map_array


class TestSuite:
    """ Class representing the whole testing suite """
    def __init__(self, tests, count, program):
        self.tests_ids = tests  # A list of available tests as their name ids
        self.tests_count = count  # Number of all tests
        self.tests = list()  # All tests where the id is equal to index
        self.program = program  # String of program name

        # Fill up the lists with unique tests
        for t in range(self.tests_count):
            self.tests.append(Test(t + 1, 0))

    @staticmethod
    def create_subset(ids_list, size):
        """ Create a subset with given test ids

        :param ids_list: ids of the desired tests as a list
        :param size: size of the subset
        :return: a new subset
        """
        subset = list()
        for i in range(size):

            subset.append(ids_list[i])
        return subset

    def create_random_subset(self, size):
        """ Same as above, just random """
        subset = random.sample(self.tests_ids, size)
        return subset

    def update_tests(self, ids, kill_ratio, subset_ids):
        """ Update test values

        :param ids: a list with test ids that killed
        :param kill_ratio: kill ratio
        :return: nothing
        """
        test_map = test_map_array('../generation/programs/' + self.program + '/testMap-' + self.program + '.csv')
        for i in range(len(ids)):
            self.tests[int(test_map[int(ids[i])]) - 1].update_kills()
            self.tests[int(test_map[int(ids[i])]) - 1].update_score(kill_ratio)
        for t in subset_ids:
            self.tests[int(t) - 1].update_selected()

    def update_wis(self, subset_ids):
        """ Update was in subset count """
        for x in subset_ids:
            self.tests[int(x) - 1].update_subset_chosen()


class TestSubset(TestSuite):
    """ Class representing the created subset """
    def __init__(self, subset_ids, count, program):
        super(TestSubset, self).__init__(subset_ids, count, program)
        self.killed = 0  # How many mutants were killed in the opposed subset

    def update_killed(self, value):
        """ Update the killed value """
        self.killed = value
