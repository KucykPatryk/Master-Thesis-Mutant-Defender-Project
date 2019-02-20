from .score import Score


# Class representing a test unit

class Test:
    def __init__(self, id, score):
        self.id = id
        self.score = Score(score)
        self.killed_times = 0  # How many times this test killed mutants
        # self.Killed_last_round = False  # True if killed a mutant in last round

    # Update the kill count
    def update_kills(self):
        self.killed_times += 1
        # print("T ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)

    # Update score
    def update_score(self, score):
        self.score.add_points(score)
        # self.survived_times += survived

        # print("T ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)
