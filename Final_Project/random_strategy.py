import random
from strategy import Strategy

class RandomStrategy(Strategy):
    """Returns random actions: hit, stand, double down, or split."""

    ACTIONS = ["hit", "stand", "double down", "split"]

    def determine_action(self, state):
        return random.choice(self.ACTIONS)
