# Class representing the point system
class Score:
    def __init__(self, points):
        self.points = points

    # Adds points by a value
    def add_points(self, value):
        self.points += value
