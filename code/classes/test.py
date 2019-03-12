from .score import Score


class Test:
    """ Class representing a test unit """
    def __init__(self, id, score):
        self.id = id
        self.score = Score(score)
        self.killed_times = 0  # How many times this test killed mutants
        # self.Killed_last_round = False  # True if killed a mutant in last round

    def update_kills(self):
        """ Update the kill count """
        self.killed_times += 1
        # print("T ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)

    def update_score(self, score):
        """ Update score """
        self.score.add_points(score)
        # self.survived_times += survived

        # print("T ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)
