import tkinter
from tkinter import ttk
from Card import Card

class Game:
    MAX_ROUNDS = 50

    def __init__(self, dealer, player):
        self.dealer = dealer
        self.dealer_hand = dealer.hand
        
        self.player = player
        self.player_hand = player.hand

        self.deck = []
        self.deck_count = 0
        self.initialize_deck()

        self.card_dict = {Card: Card.point_value for Card in self.deck}

        self.round = 1

    def initialize_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        self.deck_count = len(self.deck)

    def new_round(self):
        self.dealer.hand = self.dealer.deal_cards(self.deck, num_cards=2)
        self.dealer.total = 0

        self.player.hand = self.dealer.deal_cards(self.deck, num_cards=2)
        self.player.update_state()

        self.round += 1

    def determine_winner(self):
        player_total = self.player.get_total()
        dealer_total = self.dealer.get_total()

        while (dealer_total < 17) or (dealer_total == 17 and self.dealer.has_soft_17()):
            self.dealer.hand.append(self.dealer.deal_cards(self.deck, num_cards=1)[0])
            dealer_total = self.dealer.get_total()

        if player_total > 21:
            return 'dealer'
        elif dealer_total > 21 or player_total > dealer_total or player_total == 21:
            return 'player'
        elif dealer_total > player_total:
            return 'dealer'
        else:
            return 'draw'

    def print_round(self):
        print(f"Round: {self.round}")
        print(f"Dealer's hand: {self.dealer.hand[0].get_rank() + ' of ' + self.dealer.hand[0].suit} and [Hidden Card]")
        print(f"Player's hand: {[card.get_rank() + ' of ' + card.suit for card in self.player.hand + ' and ']}")

    def print_winner(self):
        winner = self.determine_winner()
        if winner == 'player':
            print("You win!")
        elif winner == 'dealer':
            print("You bust. Dealer wins!")
        else:
            print("You push. It's a draw!")

    def create_gui(self):
        root = tkinter.Tk()

        root.title("Blackjack Game")
        root.geometry("400x300")
        mainframe = ttk.Frame(root, padding="10")
        mainframe.grid()
        ttk.Label(mainframe, text="Welcome to Blackjack!").grid(column=1, row=1)
        root.mainloop()

        