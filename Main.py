from hashlib import new
from Game import Game
from Player import Player
from Dealer import Dealer

def main():
    dealer = Dealer()
    player = Player(new RandomStrategy())
    game = Game(dealer, player)
    msg = ""

    dealer.shuffle_deck(game.deck)

    # Initial dealing
    player.hands.append(dealer.deal_cards(game.deck, num_cards=2))
    dealer.hand = dealer.deal_cards(game.deck, num_cards=2)

    player.update_state(dealer.hand[0])

    if (game.determine_winner() == 'dealer'):
            player.update_game_status('bust')
            game.new_round()

    while (Game.MAX_ROUNDS >= game.round):
        invalid_action = True
        for i, hand in enumerate(player.hands):
            player.current_hand_index = i

            while invalid_action:
                action = str(player.determine_action()).lower()
                if action == 'hit':
                    invalid_action = player.hit(game.deck) == None
                    if invalid_action:
                        # Display message for empty deck
                        msg = "The deck is empty. Cannot hit."
                elif action == 'stand':
                    continue
                elif action == 'split':
                    invalid_action = not player.split()
                    if invalid_action:
                        # Display message for invalid split
                        msg = "Cannot split this hand."
                elif action == 'double down':
                    invalid_action = not player.double_down(game.deck)
                    if invalid_action:
                        # Display message for invalid double down
                        msg = "Cannot double down on this hand."
                # Add GUI msg popup for invalid actions if needed
            player.update_state(dealer.hand[0])
        print(msg)

if __name__ == "__main__":
    main()