from abc import ABC, abstractmethod

class Strategy(ABC):
    """Abstract base class for blackjack strategies"""
    
    @abstractmethod
    def determine_action(self, state):
        """
        Determine the action to take given the current state.
        
        Args:
            state: tuple of (player_total, dealer_visible_card, usable_ace)
        
        Returns:
            str: One of 'hit', 'stand', 'double down', 'split'
        """
        return str()  # Default action
