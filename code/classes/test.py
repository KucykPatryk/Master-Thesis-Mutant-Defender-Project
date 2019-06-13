from .score import Score


class Test:
    """ Class representing a test unit """
    def __init__(self, id, score):
        self.id = id  # Test Name ids
        self.score = Score(score)
        self.killed_times = 0  # How many times this test killed mutants
        self.subset_chosen_times = 0  # How many times it was in a subset
        self.selected = 0  # Times selected by an agent
        self.last_kill = False  # True if killed in last round it was picked

    def update_kills(self):
        """ Update the kill count """
        self.killed_times += 1
        self.last_kill = True
        # print("T ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)

    def update_score(self, score):
        """ Update score """
        self.score.add_points(score)
        # self.survived_times += survived
        # print("T ID: ", self.id, " Score: ", self.score.points, " KT: ", self.killed_times)

    def update_subset_chosen(self):
        """ Update chosen to a subset times count """
        self.subset_chosen_times += 1
        self.last_kill = False

    def update_selected(self):
        """ Update selected by agent count """
        self.selected += 1
