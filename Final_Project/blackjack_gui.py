import tkinter as tk
from tkinter import ttk
from card import Card
from dealer import Dealer
from player import Player
from game import Game
from Final_Project.basic_strategy import BasicStrategy
from random_strategy import RandomStrategy


class BlackjackGUI:
    def __init__(self, root, strategy):
        self.root = root
        self.root.title("Blackjack Simulation")
        self.root.geometry("800x600")
        self.root.configure(bg='#0D5E1F')

        # Game components
        self.dealer = Dealer()
        self.player = Player(strategy)
        self.game = Game(self.dealer, self.player)
        self.strategy = strategy

        self.dealer.shuffle_deck(self.game.deck)

        self.simulating = False
        self.delay = 700     # ms per step

        self.setup_ui()

        # Begin simulation
        self.root.after(1000, self.start_simulation)

    # UI Layout
    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg='#0D5E1F')
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="BLACKJACK SIMULATION", font=('Arial', 26, 'bold'),
                 bg='#0D5E1F', fg='white').pack()

        stats_frame = tk.Frame(self.root, bg='#0D5E1F')
        stats_frame.pack(pady=10)

        self.round_label = tk.Label(stats_frame, text="Round: 0",
                                    font=('Arial', 14), bg='#0D5E1F', fg='white')
        self.round_label.grid(row=0, column=0, padx=20)

        self.wins_label = tk.Label(stats_frame, text="Wins: 0",
                                   font=('Arial', 14), bg='#0D5E1F', fg='#4CAF50')
        self.wins_label.grid(row=0, column=1, padx=20)

        self.losses_label = tk.Label(stats_frame, text="Losses: 0",
                                     font=('Arial', 14), bg='#0D5E1F', fg='#F44336')
        self.losses_label.grid(row=0, column=2, padx=20)

        self.draws_label = tk.Label(stats_frame, text="Draws: 0",
                                    font=('Arial', 14), bg='#0D5E1F', fg='#FFC107')
        self.draws_label.grid(row=0, column=3, padx=20)

        # Dealer UI
        dealer_frame = tk.Frame(self.root, bg='#0D5E1F')
        dealer_frame.pack(pady=20)
        tk.Label(dealer_frame, text="Dealer's Hand", font=('Arial', 16, 'bold'),
                 bg='#0D5E1F', fg='white').pack()
        self.dealer_cards_label = tk.Label(dealer_frame, text="", font=('Arial', 12),
                                           bg='#0D5E1F', fg='white')
        self.dealer_cards_label.pack()
        self.dealer_total_label = tk.Label(dealer_frame, text="Total: ?", font=('Arial', 14),
                                           bg='#0D5E1F', fg='white')
        self.dealer_total_label.pack()

        # Player UI
        player_frame = tk.Frame(self.root, bg='#0D5E1F')
        player_frame.pack(pady=20)
        tk.Label(player_frame, text="Player Hand", font=('Arial', 16, 'bold'),
                 bg='#0D5E1F', fg='white').pack()
        self.player_cards_label = tk.Label(player_frame, text="", font=('Arial', 12),
                                           bg='#0D5E1F', fg='white')
        self.player_cards_label.pack()
        self.player_total_label = tk.Label(player_frame, text="Total: 0",
                                           font=('Arial', 14), bg='#0D5E1F', fg='white')
        self.player_total_label.pack()

        # Message label
        self.message_label = tk.Label(self.root, text="Starting simulation...",
                                      font=('Arial', 14, 'bold'), bg='#0D5E1F',
                                      fg='yellow')
        self.message_label.pack(pady=10)

    # GUI Helpers
    def format_card(self, card):
        suits = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        return f"{card.rank}{suits.get(card.suit, '?')}"

    def update_display(self, show_dealer=True):
        # Stats
        wins, losses, draws = self.player.game_status
        self.round_label.config(text=f"Round: {self.game.round}")
        self.wins_label.config(text=f"Wins: {wins}")
        self.losses_label.config(text=f"Losses: {losses}")
        self.draws_label.config(text=f"Draws: {draws}")

        # Dealer cards
        if show_dealer:
            dealer_cards = " ".join(self.format_card(c) for c in self.dealer.hand)
            self.dealer_total_label.config(text=f"Total: {self.dealer.get_total()}")
        else:
            dealer_cards = self.format_card(self.dealer.hand[0]) + " [Hidden]"
            self.dealer_total_label.config(text="Total: ?")
        self.dealer_cards_label.config(text=dealer_cards)

        # Player cards
        if self.player.hands:
            cards = " ".join(self.format_card(c) for c in self.player.get_current_hand())
            self.player_cards_label.config(text=cards)
            self.player_total_label.config(text=f"Total: {self.player.get_total()}")

    # Simulation Control
    def start_simulation(self):
        self.simulating = True
        self.run_round()

    def run_round(self):
        """Start a brand new round automatically."""

        # Reshuffle at 25% deck penetration
        if len(self.game.deck) < 13:
            self.game.initialize_deck()
            self.dealer.shuffle_deck(self.game.deck)
            self.message_label.config(text="Reshuffling...")

        # Reset player
        self.player.hands = []
        self.player.state = []
        self.player.doubled_down = []
        self.player.current_hand_index = 0

        # Deal cards
        self.player.hands.append(self.dealer.deal_cards(self.game.deck, 2))
        self.dealer.hand = self.dealer.deal_cards(self.game.deck, 2)
        self.player.update_state(self.dealer.hand[0])

        self.game_active = True
        self.message_label.config(text="Dealing cards...")
        self.update_display(show_dealer=False)

        # Begin player's automated turn after short delay
        self.root.after(self.delay, self.player_turn)

    def player_turn(self):
        """Automated player action determined entirely by strategy."""
        if not self.game_active:
            return

        # Ask strategy what to do
        action = self.player.determine_action().lower()

        if action == "hit":
            self.message_label.config(text="Player hits")
            self.player.hit(self.game.deck)
            self.player.update_state(self.dealer.hand[0])
            self.update_display(show_dealer=False)

            # Check bust
            if self.player.get_total() > 21:
                self.message_label.config(text="Player busts!")
                self.game_active = False
                return self.root.after(self.delay, self.finish_round)

            return self.root.after(self.delay, self.player_turn)

        elif action == "stand":
            self.message_label.config(text="Player stands")
            self.game_active = False
            return self.root.after(self.delay, self.finish_round)

        elif action == "double down":
            self.message_label.config(text="Player doubles down")
            self.player.double_down(self.game.deck)
            self.player.update_state(self.dealer.hand[0])
            self.update_display(show_dealer=False)

            # Bust check
            if self.player.get_total() > 21:
                self.message_label.config(text="Player busts after doubling!")
            self.game_active = False
            return self.root.after(self.delay, self.finish_round)

        elif action == "split":
            # BasicStrategy rarely splits, but GUI supports it.
            if self.player.can_split():
                self.message_label.config(text="Player splits")
                self.player.split()
                self.player.get_current_hand().append(self.dealer.deal_cards(self.game.deck, 1)[0])
                self.player.hands[-1].append(self.dealer.deal_cards(self.game.deck, 1)[0])
                self.player.update_state(self.dealer.hand[0])
                self.update_display(show_dealer=False)
            self.game_active = False
            return self.root.after(self.delay, self.finish_round)

        else:
            # Fallback
            self.message_label.config(text="Strategy error — default standing")
            self.game_active = False
            return self.root.after(self.delay, self.finish_round)

    def finish_round(self):
        """Dealer turn + decide winner."""
        self.update_display(show_dealer=True)

        winner = self.game.determine_winner()

        if winner == "player":
            self.message_label.config(text="Player wins!", fg="#4CAF50")
            self.player.update_game_status("win")
        elif winner == "dealer":
            self.message_label.config(text="Dealer wins!", fg="#F44336")
            self.player.update_game_status("loss")
        else:
            self.message_label.config(text="Push!", fg="#FFC107")
            self.player.update_game_status("push")

        self.game.round += 1
        self.update_display(show_dealer=True)

        # Automatically begin new round
        self.root.after(self.delay * 2, self.run_round)


def main():
    root = tk.Tk()
    strategy = BasicStrategy()   # Change to RandomStrategy() to compare
    app = BlackjackGUI(root, strategy)
    root.mainloop()


if __name__ == "__main__":
    main()
