import unittest
from card import Card
from dealer import Dealer
from player import Player
from game import Game
from basic_strategy import BasicStrategy
from random_strategy import RandomStrategy
import matplotlib.pyplot as plt
import numpy as np

class TestStrategyComparison(unittest.TestCase):
    """Compare BasicStrategy performance vs RandomStrategy"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.num_games = 1000  # Number of games to simulate
    
    def simulate_games(self, strategy, num_games):
        """
        Simulate multiple games with a given strategy
        
        Returns:
            tuple: (wins, losses, draws, win_rate, avg_reward)
        """
        dealer = Dealer()
        player = Player(strategy)
        game = Game(dealer, player)
        
        wins = 0
        losses = 0
        draws = 0
        total_reward = 0
        
        for i in range(num_games):
            # Reshuffle if deck is low (25% penetration)
            if len(game.deck) < 13:
                game.initialize_deck()
                dealer.shuffle_deck(game.deck)
            
            # Reset hands
            player.hands = []
            player.state = []
            player.doubled_down = []
            player.current_hand_index = 0
            dealer.hand = []
            
            # Deal initial cards
            player.hands.append(dealer.deal_cards(game.deck, num_cards=2))
            dealer.hand = dealer.deal_cards(game.deck, num_cards=2)
            
            # Update player state
            player.update_state(dealer.hand[0])
            
            # Player's turn
            player_done = False
            while not player_done:
                action = player.determine_action().lower()
                
                if action == 'hit':
                    card = player.hit(game.deck)
                    if not card:
                        break  # Deck empty
                    player.update_state(dealer.hand[0])
                    
                    if player.get_total() > 21:
                        player_done = True
                
                elif action == 'stand':
                    player_done = True
                
                elif action == 'double down':
                    if len(player.get_current_hand()) == 2:
                        player.double_down(game.deck)
                        player.update_state(dealer.hand[0])
                    player_done = True
                
                elif action == 'split':
                    if player.can_split():
                        player.split()
                        # For simplicity, we'll just hit once on each hand
                        player.get_current_hand().append(dealer.deal_cards(game.deck, 1)[0])
                        player.hands[-1].append(dealer.deal_cards(game.deck, 1)[0])
                        player.update_state(dealer.hand[0])
                    player_done = True
                else:
                    player_done = True
            
            # Determine winner
            winner = game.determine_winner()
            
            if winner == 'player':
                wins += 1
                total_reward += 1
            elif winner == 'dealer':
                losses += 1
                total_reward -= 1
            else:
                draws += 1
                total_reward += 0
        
        win_rate = wins / num_games if num_games > 0 else 0
        avg_reward = total_reward / num_games if num_games > 0 else 0
        
        return wins, losses, draws, win_rate, avg_reward
    
    def test_basic_strategy_outperforms_random(self):
        """Test that BasicStrategy has a higher win rate than RandomStrategy"""
        print("\n" + "="*60)
        print("STRATEGY COMPARISON TEST")
        print("="*60)
        
        # Test RandomStrategy
        print(f"\nSimulating {self.num_games} games with RandomStrategy...")
        random_strategy = RandomStrategy()
        random_wins, random_losses, random_draws, random_win_rate, random_avg_reward = \
            self.simulate_games(random_strategy, self.num_games)
        
        print(f"RandomStrategy Results:")
        print(f"  Wins: {random_wins}")
        print(f"  Losses: {random_losses}")
        print(f"  Draws: {random_draws}")
        print(f"  Win Rate: {random_win_rate:.2%}")
        print(f"  Avg Reward: {random_avg_reward:.4f}")
        
        # Test BasicStrategy
        print(f"\nSimulating {self.num_games} games with BasicStrategy...")
        basic_strategy = BasicStrategy()
        basic_wins, basic_losses, basic_draws, basic_win_rate, basic_avg_reward = \
            self.simulate_games(basic_strategy, self.num_games)
        
        print(f"\nBasicStrategy Results:")
        print(f"  Wins: {basic_wins}")
        print(f"  Losses: {basic_losses}")
        print(f"  Draws: {basic_draws}")
        print(f"  Win Rate: {basic_win_rate:.2%}")
        print(f"  Avg Reward: {basic_avg_reward:.4f}")
        
        # Calculate improvement
        win_rate_improvement = basic_win_rate - random_win_rate
        reward_improvement = basic_avg_reward - random_avg_reward
        
        print(f"\nImprovement:")
        print(f"  Win Rate Improvement: {win_rate_improvement:+.2%}")
        print(f"  Avg Reward Improvement: {reward_improvement:+.4f}")
        print("="*60)
        
        # Assert that BasicStrategy performs better
        self.assertGreater(basic_win_rate, random_win_rate,
            "BasicStrategy should have a higher win rate than RandomStrategy")
        self.assertGreater(basic_avg_reward, random_avg_reward,
            "BasicStrategy should have a higher average reward than RandomStrategy")
    
    def test_basic_strategy_consistency(self):
        """Test that BasicStrategy produces consistent results across multiple runs"""
        print("\n" + "="*60)
        print("BASIC STRATEGY CONSISTENCY TEST")
        print("="*60)
        
        basic_strategy = BasicStrategy()
        win_rates = []
        num_runs = 5
        games_per_run = 500
        
        print(f"\nRunning {num_runs} simulations of {games_per_run} games each...")
        
        for run in range(num_runs):
            _, _, _, win_rate, _ = self.simulate_games(basic_strategy, games_per_run)
            win_rates.append(win_rate)
            print(f"  Run {run + 1}: Win Rate = {win_rate:.2%}")
        
        mean_win_rate = np.mean(win_rates)
        std_win_rate = np.std(win_rates)
        
        print(f"\nMean Win Rate: {mean_win_rate:.2%}")
        print(f"Std Deviation: {std_win_rate:.4f}")
        print("="*60)
        
        # Assert reasonable consistency (std should be relatively small)
        self.assertLess(std_win_rate, 0.05,
            "Win rate should be relatively consistent across runs")
    
    def test_visualization_comparison(self):
        """Create visualizations comparing strategies (optional, for analysis)"""
        print("\n" + "="*60)
        print("GENERATING COMPARISON VISUALIZATIONS")
        print("="*60)
        
        try:
            # Run simulations
            random_strategy = RandomStrategy()
            basic_strategy = BasicStrategy()
            
            random_results = self.simulate_games(random_strategy, 1000)
            basic_results = self.simulate_games(basic_strategy, 1000)
            
            # Create comparison chart
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Win/Loss/Draw comparison
            strategies = ['Random', 'Basic']
            wins = [random_results[0], basic_results[0]]
            losses = [random_results[1], basic_results[1]]
            draws = [random_results[2], basic_results[2]]
            
            x = np.arange(len(strategies))
            width = 0.25
            
            ax1.bar(x - width, wins, width, label='Wins', color='#4CAF50')
            ax1.bar(x, losses, width, label='Losses', color='#F44336')
            ax1.bar(x + width, draws, width, label='Draws', color='#FFC107')
            
            ax1.set_xlabel('Strategy')
            ax1.set_ylabel('Number of Games')
            ax1.set_title('Game Outcomes: Random vs Basic Strategy')
            ax1.set_xticks(x)
            ax1.set_xticklabels(strategies)
            ax1.legend()
            ax1.grid(axis='y', alpha=0.3)
            
            # Win rate and average reward comparison
            metrics = ['Win Rate', 'Avg Reward']
            random_metrics = [random_results[3], random_results[4]]
            basic_metrics = [basic_results[3], basic_results[4]]
            
            x2 = np.arange(len(metrics))
            width2 = 0.35
            
            ax2.bar(x2 - width2/2, random_metrics, width2, label='Random', color='#FF9800')
            ax2.bar(x2 + width2/2, basic_metrics, width2, label='Basic', color='#2196F3')
            
            ax2.set_xlabel('Metric')
            ax2.set_ylabel('Value')
            ax2.set_title('Performance Metrics: Random vs Basic Strategy')
            ax2.set_xticks(x2)
            ax2.set_xticklabels(metrics)
            ax2.legend()
            ax2.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('strategy_comparison.png', dpi=300, bbox_inches='tight')
            print("\nVisualization saved as 'strategy_comparison.png'")
            print("="*60)
            
        except Exception as e:
            print(f"\nVisualization generation skipped: {e}")
            print("="*60)


class TestStrategyRealism(unittest.TestCase):
    """Test that strategies behave realistically in game scenarios"""
    
    def test_basic_strategy_never_hits_on_hard_20(self):
        """BasicStrategy should never hit on hard 20"""
        strategy = BasicStrategy()
        
        for dealer_value in range(2, 12):
            dealer_card = Card('Hearts', str(dealer_value) if dealer_value < 10 else 'King')
            if dealer_value == 11:
                dealer_card = Card('Hearts', 'Ace')
            
            state = (20, dealer_card, False)
            action = strategy.determine_action(state)
            
            self.assertEqual(action, 'stand',
                f"Should stand on hard 20 vs dealer {dealer_value}")
    
    def test_basic_strategy_hits_on_low_totals(self):
        """BasicStrategy should hit on low totals (< 12)"""
        strategy = BasicStrategy()
        
        for total in range(5, 11):
            dealer_card = Card('Hearts', '7')
            state = (total, dealer_card, False)
            action = strategy.determine_action(state)
            
            self.assertIn(action, ['hit', 'double down'],
                f"Should hit or double on hard {total}")
    
    def test_random_strategy_generates_all_actions(self):
        """RandomStrategy should be able to generate all action types"""
        strategy = RandomStrategy()
        
        actions_generated = set()
        dealer_card = Card('Hearts', '7')
        state = (15, dealer_card, False)
        
        # Generate 100 actions, should see variety
        for _ in range(100):
            action = strategy.determine_action(state)
            actions_generated.add(action)
        
        # Should have generated at least 3 different actions
        self.assertGreaterEqual(len(actions_generated), 3,
            "RandomStrategy should generate multiple different actions")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
