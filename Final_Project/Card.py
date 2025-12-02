class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        self.point_value = self.assign_point_value()

    def assign_point_value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11
        else:
            return int(self.rank)
        
    def get_rank(self):
        return self.rank