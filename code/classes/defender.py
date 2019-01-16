from subprocess import run


class Defender:
    def __init__(self):
        return

    # Generates mutants with context and log files
    @staticmethod
    def generate_tests():
        run(['./' + 'run_tests_generation.sh'], cwd='../generation/')