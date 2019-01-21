from subprocess import run

from .test_suite import TestSuite
from .test_suite import TestSubset

from .global_variables import *


class Defender:
    def __init__(self):
        self.tests_ids = self.read_test_ids()
        self.t_suite = TestSuite(self.tests_ids, len(self.tests_ids))

    # Generates mutants with context and log files
    @staticmethod
    def generate_tests():
        run(['./' + 'run_tests_generation.sh'], cwd='../generation/')

    # Reads test ids from the java file with tests and save it as a list
    @staticmethod
    def read_test_ids():
        ids = list()
        with open('../generation/evosuite-tests/triangle/Triangle_ESTest.java') as f:
            for line in f:
                if line[:13] in '  public void':
                    ln = line.split()
                    tn = ln[2].split('(')[0]
                    ids.append(tn)
        return ids
