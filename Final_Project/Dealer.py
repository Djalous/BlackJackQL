class Dealer:
    def __init__(self):
        self.hand = []
        self.total = 0

    def deal_cards(self, deck, num_cards=1):
        dealt_cards = []
        for _ in range(num_cards):
            if deck:
                dealt_cards.append(deck.pop())
            else:
                break
        return dealt_cards
    
    def shuffle_deck(self, deck):
        import random
        random.shuffle(deck)

    def get_total(self):
        total = 0

        for card in self.hand:
            total += card.point_value
        self.total = total
        return self.total
    
    def has_soft_17(self):
        has_ace = any(card.rank == 'Ace' for card in self.hand)
        return has_ace and self.get_total() == 17