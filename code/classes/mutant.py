from .score import Score


class Mutant:
    """ Class representing a mutant unit """
    def __init__(self, id, score):
        self.id = id
        self.score = Score(score)
        # self.survived_times = 0  # How many times this mutant survived
        self.killed_times = 0  # How many times this mutant was killed
        # self.survive_last_round = False  # True if survived in last round

    def update_kills(self):
        """ Update the kill count """
        self.killed_times += 1
        # print("M ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)

    def update_score(self, score):
        """ Update score """
        self.score.add_points(score)
        # self.survived_times += survived

        # print("M ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)
