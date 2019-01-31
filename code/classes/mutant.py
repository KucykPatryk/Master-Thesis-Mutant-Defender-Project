from .score import Score


# Class representing a mutant unit

class Mutant:
    def __init__(self, id, score):
        self.id = id
        self.score = Score(score)
        # self.survived_times = 0  # How many times this mutant survived
        self.killed_times = 0  # How many times this mutant was killed
        # self.survive_last_round = False  # True if survived in last round

    # Updates values of this mutant
    def update_values(self, score):
        self.score.add_points(score)
        # self.survived_times += survived
        self.killed_times += 1

        # print("ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)
