class Player:
    def __init__(self, strategy):
        self.hands = [] # For handling multiple hands in case of splits
        self.current_hand_index = 0
        self.state = [] # (player_total, dealer_visible_card, usable_ace)
        self.game_status = (0, 0, 0)  # (wins, losses, draws)
        self.strategy = strategy  # Placeholder for strategy implementation

    def get_current_hand(self):
        return self.hands[self.current_hand_index]

    def hit(self, deck):
        card = deck.pop() if deck else None
        if card:
            self.get_current_hand().append(card)
        return card
    
    def can_split(self):
        hand = self.get_current_hand()
        return len(hand) == 2 and hand[0].get_rank() == hand[1].get_rank()
    
    def split(self):
        if not self.can_split():
            return False
        hand = self.get_current_hand()
        new_hand = [hand.pop()]
        self.hands.append(new_hand)
        return True
    
    def double_down(self, deck):
        hand = self.get_current_hand()
        if len(hand) == 2:
            self.hit(deck)
            # Mark that the bet is doubled
            if not hasattr(self, 'doubled_down'):
                self.doubled_down = [False] * len(self.hands)
                return True
            self.doubled_down[self.current_hand_index] = True
        return False

    def update_state(self, dealer_visible_card):
        total = 0
        ace_count = 0

        for card in self.hands[self.current_hand_index]:
            total += card.point_value
            if card.rank == 'Ace':
                ace_count += 1

        # Adjust for usable aces
        while total > 21 and ace_count:
            total -= 10
            ace_count -= 1

        usable_ace = ace_count > 0
        self.state[self.current_hand_index] = (total, dealer_visible_card, usable_ace)

    def determine_action(self):
        return self.strategy.determine_action(self.state[self.current_hand_index])
        
    def update_game_status(self, result):
        wins, losses, draws = self.game_status
        if result == 'win':
            wins += 1
        elif result == 'bust':
            losses += 1
        elif result == 'push':
            draws += 1
        self.game_status = (wins, losses, draws)