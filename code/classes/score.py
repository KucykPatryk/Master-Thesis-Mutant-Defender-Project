class Score:
    """ Class representing a point unit """
    def __init__(self, points):
        self.points = points

    def add_points(self, value):
        """ Add points by a value """
        self.points += value
