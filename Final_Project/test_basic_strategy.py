import unittest
from card import Card
from basic_strategy import BasicStrategy

class TestBasicStrategy(unittest.TestCase):
    """Test the BasicStrategy implementation against the strategy chart"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.strategy = BasicStrategy()
    
    def test_hard_17_plus_always_stand(self):
        """Test that hard 17+ always stands"""
        for total in range(17, 22):
            for dealer_value in range(2, 12):
                dealer_card = self._create_card_from_value(dealer_value)
                state = (total, dealer_card, False)  # False = no usable ace
                action = self.strategy.determine_action(state)
                self.assertEqual(action, 'stand', 
                    f"Hard {total} vs dealer {dealer_value} should stand")
    
    def test_hard_16_stands_on_2_6(self):
        """Test hard 16 stands on dealer 2-6"""
        for dealer_value in range(2, 7):
            dealer_card = self._create_card_from_value(dealer_value)
            state = (16, dealer_card, False)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'stand',
                f"Hard 16 vs dealer {dealer_value} should stand")
    
    def test_hard_16_hits_on_7_ace(self):
        """Test hard 16 hits on dealer 7-A"""
        for dealer_value in range(7, 12):
            dealer_card = self._create_card_from_value(dealer_value)
            state = (16, dealer_card, False)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'hit',
                f"Hard 16 vs dealer {dealer_value} should hit")
    
    def test_hard_12_strategy(self):
        """Test hard 12 strategy: Hit on 2-3, Stand on 4-6, Hit on 7-A"""
        # Hit on 2-3
        for dealer_value in [2, 3]:
            dealer_card = self._create_card_from_value(dealer_value)
            state = (12, dealer_card, False)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'hit',
                f"Hard 12 vs dealer {dealer_value} should hit")
        
        # Stand on 4-6
        for dealer_value in range(4, 7):
            dealer_card = self._create_card_from_value(dealer_value)
            state = (12, dealer_card, False)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'stand',
                f"Hard 12 vs dealer {dealer_value} should stand")
        
        # Hit on 7-A
        for dealer_value in range(7, 12):
            dealer_card = self._create_card_from_value(dealer_value)
            state = (12, dealer_card, False)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'hit',
                f"Hard 12 vs dealer {dealer_value} should hit")
    
    def test_hard_11_always_double(self):
        """Test that hard 11 always doubles"""
        for dealer_value in range(2, 12):
            dealer_card = self._create_card_from_value(dealer_value)
            state = (11, dealer_card, False)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'double down',
                f"Hard 11 vs dealer {dealer_value} should double")
    
    def test_hard_10_doubles_on_2_9(self):
        """Test hard 10 doubles on dealer 2-9, hits on 10-A"""
        # Double on 2-9
        for dealer_value in range(2, 10):
            dealer_card = self._create_card_from_value(dealer_value)
            state = (10, dealer_card, False)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'double down',
                f"Hard 10 vs dealer {dealer_value} should double")
        
        # Hit on 10-A
        for dealer_value in [10, 11]:
            dealer_card = self._create_card_from_value(dealer_value)
            state = (10, dealer_card, False)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'hit',
                f"Hard 10 vs dealer {dealer_value} should hit")
    
    def test_soft_19_always_stands(self):
        """Test that soft 19 (A,8) always stands"""
        for dealer_value in range(2, 12):
            dealer_card = self._create_card_from_value(dealer_value)
            state = (19, dealer_card, True)  # True = usable ace
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'stand',
                f"Soft 19 vs dealer {dealer_value} should stand")
    
    def test_soft_18_strategy(self):
        """Test soft 18 (A,7) strategy"""
        # Stand on 2, 7, 8
        for dealer_value in [2, 7, 8]:
            dealer_card = self._create_card_from_value(dealer_value)
            state = (18, dealer_card, True)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'stand',
                f"Soft 18 vs dealer {dealer_value} should stand")
        
        # Hit on 9, 10
        for dealer_value in [9, 10]:
            dealer_card = self._create_card_from_value(dealer_value)
            state = (18, dealer_card, True)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'hit',
                f"Soft 18 vs dealer {dealer_value} should hit")
    
    def test_soft_17_doubles_on_3_6(self):
        """Test soft 17 (A,6) doubles on 3-6"""
        for dealer_value in range(3, 7):
            dealer_card = self._create_card_from_value(dealer_value)
            state = (17, dealer_card, True)
            action = self.strategy.determine_action(state)
            self.assertEqual(action, 'double down',
                f"Soft 17 vs dealer {dealer_value} should double")
    
    def test_soft_13_to_15_double_on_4_6(self):
        """Test soft 13-15 double on dealer 4-6"""
        for total in [13, 14, 15]:
            for dealer_value in range(4, 7):
                dealer_card = self._create_card_from_value(dealer_value)
                state = (total, dealer_card, True)
                action = self.strategy.determine_action(state)
                self.assertEqual(action, 'double down',
                    f"Soft {total} vs dealer {dealer_value} should double")
    
    def test_pair_aces_always_split(self):
        """Test that pair of aces always splits"""
        for dealer_value in range(2, 12):
            dealer_card = self._create_card_from_value(dealer_value)
            action = self.strategy.determine_action_for_pair('Ace', dealer_card)
            self.assertEqual(action, 'split',
                f"Pair of Aces vs dealer {dealer_value} should split")
    
    def test_pair_eights_always_split(self):
        """Test that pair of 8s always splits"""
        for dealer_value in range(2, 12):
            dealer_card = self._create_card_from_value(dealer_value)
            action = self.strategy.determine_action_for_pair('8', dealer_card)
            self.assertEqual(action, 'split',
                f"Pair of 8s vs dealer {dealer_value} should split")
    
    def test_pair_tens_never_split(self):
        """Test that pair of 10s never splits (always stands)"""
        for dealer_value in range(2, 12):
            dealer_card = self._create_card_from_value(dealer_value)
            action = self.strategy.determine_action_for_pair('10', dealer_card)
            self.assertEqual(action, 'stand',
                f"Pair of 10s vs dealer {dealer_value} should stand")
    
    def test_pair_nines_strategy(self):
        """Test pair of 9s: split on 2-6, 8-9, stand on 7, 10, A"""
        # Split on 2-6
        for dealer_value in range(2, 7):
            dealer_card = self._create_card_from_value(dealer_value)
            action = self.strategy.determine_action_for_pair('9', dealer_card)
            self.assertEqual(action, 'split',
                f"Pair of 9s vs dealer {dealer_value} should split")
        
        # Stand on 7, 10, A
        for dealer_value in [7, 10, 11]:
            dealer_card = self._create_card_from_value(dealer_value)
            action = self.strategy.determine_action_for_pair('9', dealer_card)
            self.assertEqual(action, 'stand',
                f"Pair of 9s vs dealer {dealer_value} should stand")
        
        # Split on 8-9
        for dealer_value in [8, 9]:
            dealer_card = self._create_card_from_value(dealer_value)
            action = self.strategy.determine_action_for_pair('9', dealer_card)
            self.assertEqual(action, 'split',
                f"Pair of 9s vs dealer {dealer_value} should split")
    
    def test_pair_fives_never_split(self):
        """Test pair of 5s: double on 2-9, hit on 10-A"""
        # Double on 2-9
        for dealer_value in range(2, 10):
            dealer_card = self._create_card_from_value(dealer_value)
            action = self.strategy.determine_action_for_pair('5', dealer_card)
            self.assertEqual(action, 'double down',
                f"Pair of 5s vs dealer {dealer_value} should double")
        
        # Hit on 10-A
        for dealer_value in [10, 11]:
            dealer_card = self._create_card_from_value(dealer_value)
            action = self.strategy.determine_action_for_pair('5', dealer_card)
            self.assertEqual(action, 'hit',
                f"Pair of 5s vs dealer {dealer_value} should hit")
    
    def _create_card_from_value(self, value):
        """Helper to create a card from a numeric value"""
        if value == 11:
            return Card('Hearts', 'Ace')
        elif value == 10:
            return Card('Hearts', 'King')
        else:
            return Card('Hearts', str(value))
    
    def test_normalize_dealer_card(self):
        """Test that dealer card normalization works correctly"""
        # Test with Card objects
        ace = Card('Hearts', 'Ace')
        self.assertEqual(self.strategy._normalize_dealer_card(ace), 11)
        
        king = Card('Spades', 'King')
        self.assertEqual(self.strategy._normalize_dealer_card(king), 10)
        
        five = Card('Diamonds', '5')
        self.assertEqual(self.strategy._normalize_dealer_card(five), 5)
        
        # Test with numeric values
        self.assertEqual(self.strategy._normalize_dealer_card(7), 7)


if __name__ == '__main__':
    unittest.main(verbosity=2)
