from subprocess import run


class Attacker:
    def __init__(self):
        return

    # Generates mutants with context and log files
    @staticmethod
    def generate_mutants():
        run(['./' + 'run_mutant_generation.sh'], cwd='../generation/')



