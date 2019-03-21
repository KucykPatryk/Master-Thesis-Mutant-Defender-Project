from .score import Score


class Mutant:
    """ Class representing a mutant unit """
    def __init__(self, id, score):
        self.id = id
        self.score = Score(score)
        self.survived_times = 0  # How many times this mutant survived
        self.killed_times = 0  # How many times this mutant was killed
        self.subset_chosen_times = 0  # How many times it was in a subset
        self.selected = 0  # Times selected by an agent

    def update_kills(self):
        """ Update the kill count """
        self.killed_times += 1
        # print("M ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)

    def update_score(self, score):
        """ Update score """
        self.score.add_points(score)
        # self.survived_times += survived

        # print("M ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)

    def update_survived(self):
        """ Update survived count """
        self.survived_times += 1

    def update_subset_chosen(self):
        """ Update chosen to a subset times count """
        self.subset_chosen_times += 1

    def update_selected(self):
        """ Update selected by agent count """
        self.selected += 1
