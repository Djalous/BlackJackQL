class Player:
    def __init__(self, strategy):
        self.hands = []  # For handling multiple hands in case of splits
        self.current_hand_index = 0
        self.state = []  # list of tuples: (player_total, dealer_visible_card, usable_ace)
        self.game_status = (0, 0, 0)  # (wins, losses, draws)
        self.strategy = strategy  # Placeholder for strategy implementation
        self.doubled_down = []  # parallel list to track which hands were doubled

    def get_current_hand(self):
        return self.hands[self.current_hand_index]

    def hit(self, deck):
        card = deck.pop() if deck else None
        if card:
            self.get_current_hand().append(card)
        return card

    def _card_rank(self, card):
        """Safe rank getter: use get_rank() if present, else .rank attribute."""
        if hasattr(card, 'get_rank'):
            return card.get_rank()
        return getattr(card, 'rank', None)

    def can_split(self):
        hand = self.get_current_hand()
        if len(hand) != 2:
            return False
        rank0 = self._card_rank(hand[0])
        rank1 = self._card_rank(hand[1])
        return rank0 is not None and rank0 == rank1

    def split(self):
        if not self.can_split():
            return False
        hand = self.get_current_hand()
        # Pop one card and make a new hand with it
        new_hand = [hand.pop()]
        self.hands.append(new_hand)
        # Maintain doubled_down parallel list
        if len(self.doubled_down) < len(self.hands):
            self.doubled_down.append(False)
        # Maintain state parallel list (placeholder for new hand)
        if len(self.state) < len(self.hands):
            self.state.append((0, None, False))
        return True

    def double_down(self, deck):
        """
        Perform double down: allowed only on 2-card hands.
        Returns True if double down performed, False otherwise.
        """
        hand = self.get_current_hand()
        if len(hand) == 2:
            card = self.hit(deck)
            # ensure doubled_down list is long enough
            while len(self.doubled_down) < len(self.hands):
                self.doubled_down.append(False)
            self.doubled_down[self.current_hand_index] = True
            return True
        return False

    def update_state(self, dealer_visible_card):
        """
        Compute total and usable_ace for the current hand and update self.state
        for current_hand_index. Will append to state list if needed.
        """
        hand = self.get_current_hand()
        total = 0
        ace_count = 0

        # Sum values, counting Aces as 11 initially (assuming card.point_value uses 11 for Ace)
        # If card.point_value uses 1 for Ace, adapt accordingly. This code assumes Ace=11 in point_value.
        for card in hand:
            # fall back to attribute names used in different Card implementations
            if hasattr(card, 'point_value'):
                val = card.point_value
            else:
                # try to infer numeric value from rank if point_value not present
                rank = str(getattr(card, 'rank', None))
                if rank == 'Ace':
                    val = 11
                elif rank in ['King', 'Queen', 'Jack']:
                    val = 10
                else:
                    try:
                        val = int(rank)
                    except Exception:
                        val = 0
            total += val
            if getattr(card, 'rank', None) == 'Ace':
                ace_count += 1

        # Reduce Aces from 11 to 1 as needed
        reductions = 0
        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1
            reductions += 1

        # usable_ace is True if at least one Ace is still counted as 11
        # (i.e., original_ace_count - reductions > 0)
        # To compute original_ace_count: it's reductions + ace_count (after reductions)
        # So usable_ace = (reductions + ace_count) - reductions > 0 => ace_count > 0 after all reductions
        # But above ace_count was decremented down; recompute in simpler form:
        # We'll inspect the hand directly for original ace count.
        original_ace_count = sum(1 for c in hand if getattr(c, 'rank', None) == 'Ace')
        usable_ace = (original_ace_count - reductions) > 0

        # Ensure state list is long enough then assign
        while len(self.state) <= self.current_hand_index:
            self.state.append((0, None, False))
        self.state[self.current_hand_index] = (total, dealer_visible_card, usable_ace)

    def determine_action(self):
        """
        Ask the strategy for action based on the stored state of the current hand.
        It is expected that update_state(dealer_upcard) was called prior to this.
        """
        # Defensive: if state not prepared, fallback to computing total with no dealer card
        if len(self.state) <= self.current_hand_index:
            # create a quick state using get_total() and no dealer upcard
            total = self.get_total(self.current_hand_index)
            fake_dealer = None
            usable = False
            self.state.append((total, fake_dealer, usable))

        return self.strategy.determine_action(self.state[self.current_hand_index])

    def get_total(self, hand_index=None):
        """
        Return the numeric total of the specified hand (or current hand if None).
        Accounts for Ace being 11 or 1 to avoid bust when possible.
        """
        if hand_index is None:
            hand_index = self.current_hand_index
        if hand_index < 0 or hand_index >= len(self.hands):
            return 0
        hand = self.hands[hand_index]

        total = 0
        ace_count = 0
        for card in hand:
            if hasattr(card, 'point_value'):
                val = card.point_value
            else:
                rank = str(getattr(card, 'rank', None))
                if rank == 'Ace':
                    val = 11
                elif rank in ['King', 'Queen', 'Jack']:
                    val = 10
                else:
                    try:
                        val = int(rank)
                    except Exception:
                        val = 0
            total += val
            if getattr(card, 'rank', None) == 'Ace':
                ace_count += 1

        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1

        return total

    def update_game_status(self, result):
        wins, losses, draws = self.game_status
        if result == 'win':
            wins += 1
        elif result == 'bust' or result == 'loss' or result == 'dealer':
            losses += 1
        elif result == 'push' or result == 'draw':
            draws += 1
        self.game_status = (wins, losses, draws)
