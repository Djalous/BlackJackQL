import unittest
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

from dealer import Dealer
from player import Player
from game import Game
from basic_strategy import BasicStrategy
from random_strategy import RandomStrategy
from qlearning_strategy import QLearningStrategy
from card import Card


class StrategyTestBase(unittest.TestCase):
    """Base class containing shared game simulation logic."""

    def simulate_games(self, strategy, num_games):
        """
        Simulate blackjack games for any strategy.

        Returns:
            (wins, losses, draws, win_rate, avg_reward, rewards_list)
        """
        dealer = Dealer()
        player = Player(strategy)
        game = Game(dealer, player)

        wins = losses = draws = 0
        rewards = []

        for _ in range(num_games):
            # Reshuffle when deck reaches 25%
            if len(game.deck) < 13:
                game.initialize_deck()
                dealer.shuffle_deck(game.deck)

            # Reset states
            player.hands = []
            player.state = []
            player.doubled_down = []
            player.current_hand_index = 0
            dealer.hand = []

            # Deal initial cards
            player.hands.append(dealer.deal_cards(game.deck, 2))
            dealer.hand = dealer.deal_cards(game.deck, 2)
            player.update_state(dealer.hand[0])

            # Player turn
            done = False
            while not done:
                action = player.determine_action().lower()

                if action == "hit":
                    card = player.hit(game.deck)
                    player.update_state(dealer.hand[0])

                    if player.get_total() > 21:
                        done = True

                elif action == "stand":
                    done = True

                elif action == "double down":
                    if len(player.get_current_hand()) == 2:
                        player.double_down(game.deck)
                        player.update_state(dealer.hand[0])
                    done = True

                elif action == "split":
                    if player.can_split():
                        player.split()
                        player.get_current_hand().append(dealer.deal_cards(game.deck, 1)[0])
                        player.hands[-1].append(dealer.deal_cards(game.deck, 1)[0])
                    done = True

                else:
                    done = True

            # Winner evaluation
            winner = game.determine_winner()

            if winner == "player":
                wins += 1
                rewards.append(1)
            elif winner == "dealer":
                losses += 1
                rewards.append(-1)
            else:
                draws += 1
                rewards.append(0)

        win_rate = wins / num_games
        avg_reward = np.mean(rewards)

        return wins, losses, draws, win_rate, avg_reward, rewards


# ---------------------------------------------------------------------
#  Q-LEARNING VS BASIC STRATEGY PERFORMANCE
# ---------------------------------------------------------------------

class TestStrategyComparisonQlearning(StrategyTestBase):
    """Compare QLearningStrategy vs BasicStrategy."""

    def setUp(self):
        self.num_games = 10_000  # Requirement: 10k games

    def test_qlearning_outperforms_basic(self):
        print("\n" + "="*80)
        print("Q-LEARNING vs BASIC STRATEGY — PERFORMANCE TEST")
        print("="*80)

        q_strategy = QLearningStrategy(learning_rate=0.1, discount_factor=0.95, exploration_rate=0.05)
        basic_strategy = BasicStrategy()

        # Simulate games
        print("\nSimulating Q-Learning Strategy...")
        q_wins, q_losses, q_draws, q_win_rate, q_avg_reward, q_rewards = \
            self.simulate_games(q_strategy, self.num_games)

        print(f"Q-Learning:\n  Win Rate: {q_win_rate:.2%}\n  Avg Reward: {q_avg_reward:.4f}")

        print("\nSimulating Basic Strategy...")
        b_wins, b_losses, b_draws, b_win_rate, b_avg_reward, b_rewards = \
            self.simulate_games(basic_strategy, self.num_games)

        print(f"Basic Strategy:\n  Win Rate: {b_win_rate:.2%}\n  Avg Reward: {b_avg_reward:.4f}")

        # ----------------------------------------------------------------------------------
        # Statistical significance test (two-sample t-test)
        # ----------------------------------------------------------------------------------
        t_stat, p_value = ttest_ind(q_rewards, b_rewards, equal_var=False)
        print("\nT-TEST COMPARISON (Q-Learning vs Basic)")
        print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.6f}")

        # p < 0.05 → significant difference
        self.assertLess(p_value, 0.05,
            "Q-Learning should differ significantly from Basic Strategy (p < 0.05).")

        # Expect Q-learning to eventually outperform
        self.assertGreater(q_win_rate, b_win_rate,
            "Q-Learning should have a higher win rate than Basic Strategy.")
        self.assertGreater(q_avg_reward, b_avg_reward,
            "Q-Learning should have a higher average reward than Basic Strategy.")


# ---------------------------------------------------------------------
#  Q-LEARNING STRATEGY SANITY TESTS
# ---------------------------------------------------------------------

class TestQLearningStrategyBehavior(unittest.TestCase):
    """Behavior-level tests to ensure QLearningStrategy behaves reasonably."""

    def test_qlearning_returns_valid_actions(self):
        strategy = QLearningStrategy()
        dealer_card = Card("Hearts", "9")
        state = (15, dealer_card, False)

        action = strategy.determine_action(state)
        self.assertIn(action, ["hit", "stand", "double down", "split"],
                      "Q-Learning must return a valid blackjack action.")

    def test_qlearning_updates_qvalues(self):
        strategy = QLearningStrategy()

        s = (14, Card("Spades", "6"), False)
        a = "hit"
        r = 1
        s_next = (19, Card("Spades", "6"), False)

        old_q = strategy.get_Q(s, a)
        strategy.update_Q(s, a, r, s_next)

        self.assertNotEqual(strategy.get_Q(s, a), old_q,
                            "Q-Learning must update Q-values after experience.")


# ---------------------------------------------------------------------
#  Q-VALUE AND POLICY VISUALIZATION
# ---------------------------------------------------------------------

class TestQValueVisualization(unittest.TestCase):
    """Generate heatmaps and policy visual comparisons."""

    def test_qvalue_heatmap(self):
        print("\nGenerating Q-value heatmap...")

        strategy = QLearningStrategy()
        Q = strategy.get_Q_table()

        # Build heatmap grid: rows = player totals, columns = dealer upcards
        totals = range(4, 22)
        dealer_cards = range(2, 12)  # Using numeric upcard values

        heatmap = np.zeros((len(totals), len(dealer_cards)))

        for i, t in enumerate(totals):
            for j, d in enumerate(dealer_cards):
                # Choose best action Q(s,a)
                s = (t, Card("Clubs", str(d) if d < 11 else "Ace"), False)
                actions = ["hit", "stand", "double down"]
                heatmap[i, j] = max(strategy.get_Q(s, a) for a in actions)

        plt.imshow(heatmap, cmap="viridis", origin="lower")
        plt.xlabel("Dealer Upcard (2–A)")
        plt.ylabel("Player Total (4–21)")
        plt.title("Q-Learning — Max Q-value Heatmap")
        plt.colorbar(label="Q-value")
        plt.savefig("qlearning_qvalue_heatmap.png", dpi=300)
        plt.close()

        print("Saved: qlearning_qvalue_heatmap.png")

    def test_qlearning_vs_basic_policy_chart(self):
        print("\nGenerating policy comparison chart...")

        q = QLearningStrategy()
        b = BasicStrategy()

        totals = list(range(8, 18))
        dealer_upcards = list(range(2, 12))

        fig, ax = plt.subplots(figsize=(14, 8))

        q_policy = []
        b_policy = []

        for t in totals:
            row_q = []
            row_b = []
            for d in dealer_upcards:
                card = Card("Spades", str(d) if d < 11 else "Ace")
                s = (t, card, False)
                row_q.append(q.determine_action(s))
                row_b.append(b.determine_action(s))
            q_policy.append(row_q)
            b_policy.append(row_b)

        ax.set_title("Policy Comparison: Q-Learning vs Basic Strategy", fontsize=16)
        ax.set_axis_off()

        plt.savefig("qlearning_vs_basic_policy.png", dpi=300)
        plt.close()

        print("Saved: qlearning_vs_basic_policy.png")


# ---------------------------------------------------------------------
#  MAIN ENTRY
# ---------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main(verbosity=2)
