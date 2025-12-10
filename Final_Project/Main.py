from game import Game
from player import Player
from dealer import Dealer
from random_strategy import RandomStrategy
from basic_strategy import BasicStrategy

def main():
    # Choose strategy: RandomStrategy or BasicStrategy
    # strategy = RandomStrategy()
    strategy = BasicStrategy()
    
    dealer = Dealer()
    player = Player(strategy)
    game = Game(dealer, player)
    
    dealer.shuffle_deck(game.deck)

    # Initial dealing
    player.hands = [dealer.deal_cards(game.deck, num_cards=2)]
    player.current_hand_index = 0
    dealer.hand = dealer.deal_cards(game.deck, num_cards=2)

    player.update_state(dealer.hand[0])

    # Play rounds
    round_count = 0
    while round_count < Game.MAX_ROUNDS and len(game.deck) >= 13:
        game.print_round()
        
        # Player's turn - handle all hands (in case of splits)
        for hand_index in range(len(player.hands)):
            player.current_hand_index = hand_index
            
            if len(player.hands) > 1:
                print(f"\nPlaying hand {hand_index + 1} of {len(player.hands)}")
            
            # Player makes decisions
            while True:
                player_total = player.get_total()
                
                # Check if player busts
                if player_total > 21:
                    print(f"Hand busts with {player_total}!")
                    break
                
                # Determine action
                action = player.determine_action().lower()
                print(f"Player chooses to: {action}")
                
                if action == 'hit':
                    card = player.hit(game.deck)
                    if not card:
                        print("Deck is empty. Cannot hit.")
                        break
                    player.update_state(dealer.hand[0])
                    print(f"Drew: {card.get_rank()} of {card.suit}")
                    
                elif action == 'stand':
                    print("Player stands.")
                    break
                    
                elif action == 'split':
                    if player.can_split() and len(player.get_current_hand()) == 2:
                        if player.split():
                            print("Hand split!")
                            # Deal one card to each split hand
                            player.get_current_hand().append(dealer.deal_cards(game.deck, 1)[0])
                            player.hands[-1].append(dealer.deal_cards(game.deck, 1)[0])
                            player.update_state(dealer.hand[0])
                        else:
                            print("Cannot split this hand.")
                            # Fallback to hit if split fails
                            action = 'hit'
                            continue
                    else:
                        print("Cannot split. Hitting instead.")
                        card = player.hit(game.deck)
                        if card:
                            player.update_state(dealer.hand[0])
                    
                elif action == 'double down':
                    if len(player.get_current_hand()) == 2:
                        if player.double_down(game.deck):
                            print("Doubled down!")
                            player.update_state(dealer.hand[0])
                            break  # Turn ends after double down
                        else:
                            print("Cannot double down. Deck might be empty.")
                    else:
                        print("Can only double down on initial 2-card hand. Hitting instead.")
                        card = player.hit(game.deck)
                        if card:
                            player.update_state(dealer.hand[0])
                else:
                    # Unknown action, default to stand
                    print("Unknown action. Standing.")
                    break
        
        # Determine winner
        print("\nDealer's turn...")
        print(f"Dealer reveals: {dealer.hand[1].get_rank()} of {dealer.hand[1].suit}")
        
        winner = game.determine_winner()
        game.print_winner()
        
        # Update game status
        if winner == 'player':
            player.update_game_status('win')
        elif winner == 'dealer':
            player.update_game_status('bust' if player.get_total() > 21 else 'loss')
        else:
            player.update_game_status('push')
        
        # Print current statistics
        wins, losses, draws = player.game_status
        print(f"\nCurrent Stats - Wins: {wins}, Losses: {losses}, Draws: {draws}")
        print("-" * 60)
        
        # Start new round
        if len(game.deck) >= 13 and round_count < Game.MAX_ROUNDS - 1:
            game.new_round()
            round_count += 1
        else:
            break
    
    # Final statistics
    wins, losses, draws = player.game_status
    total_games = wins + losses + draws
    win_rate = wins / total_games if total_games > 0 else 0
    
    print("\n" + "=" * 60)
    print("GAME OVER - Final Statistics")
    print("=" * 60)
    print(f"Total Rounds Played: {total_games}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Draws: {draws}")
    print(f"Win Rate: {win_rate:.2%}")
    print("=" * 60)

if __name__ == "__main__":
    main()