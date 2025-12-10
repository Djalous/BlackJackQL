from card import Card

class Game:
    MAX_ROUNDS = 50

    def __init__(self, dealer, player):
        self.dealer = dealer
        self.dealer_hand = dealer.hand
        
        self.player = player
        self.player_hand = player.hands  # Changed to hands (plural) for split support

        self.deck = []
        self.deck_count = 0
        self.initialize_deck()

        self.round = 1

    def initialize_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        self.deck_count = len(self.deck)

    def new_round(self):
        self.dealer.hand = self.dealer.deal_cards(self.deck, num_cards=2)
        self.dealer.total = 0

        self.player.hands = [self.dealer.deal_cards(self.deck, num_cards=2)]
        self.player.current_hand_index = 0
        self.player.state = []
        self.player.doubled_down = []
        self.player.update_state(self.dealer.hand[0])

        self.round += 1

    def determine_winner(self):
        player_total = self.player.get_total()
        dealer_total = self.dealer.get_total()

        # Dealer hits on soft 17 or any total less than 17
        while (dealer_total < 17) or (dealer_total == 17 and self.dealer.has_soft_17()):
            new_card = self.dealer.deal_cards(self.deck, num_cards=1)
            if new_card:
                self.dealer.hand.append(new_card[0])
                dealer_total = self.dealer.get_total()
            else:
                break  # Deck is empty

        if player_total > 21:
            return 'dealer'
        elif dealer_total > 21:
            return 'player'
        elif player_total == 21 and len(self.player.get_current_hand()) == 2:
            # Player has blackjack
            if dealer_total == 21 and len(self.dealer.hand) == 2:
                return 'draw'  # Both have blackjack
            return 'player'
        elif player_total > dealer_total:
            return 'player'
        elif dealer_total > player_total:
            return 'dealer'
        else:
            return 'draw'

    def print_round(self):
        """Print the current round information"""
        print(f"Round: {self.round}")
        
        if self.dealer.hand:
            print(f"Dealer's hand: {self.dealer.hand[0].get_rank()} of {self.dealer.hand[0].suit} and [Hidden Card]")
        
        if self.player.hands and len(self.player.hands) > 0:
            current_hand = self.player.get_current_hand()
            cards_str = ", ".join([f"{card.get_rank()} of {card.suit}" for card in current_hand])
            print(f"Player's hand: {cards_str}")

    def print_winner(self):
        """Print the winner of the round"""
        winner = self.determine_winner()
        if winner == 'player':
            print("You win!")
        elif winner == 'dealer':
            player_total = self.player.get_total()
            if player_total > 21:
                print("You bust. Dealer wins!")
            else:
                print("Dealer wins!")
        else:
            print("Push! It's a draw!")