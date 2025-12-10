# BlackJackQL

This project implements a Blackjack game with multiple strategies including Random and Basic Strategy, along with a GUI and comprehensive testing suite.

## Project Structure
├── Card.py                      # Card class definition
├── Dealer.py                    # Dealer class with game logic
├── Player.py (Fixed)            # Player class with strategy support
├── Game.py (Fixed)              # Game orchestration
├── Main.py (Fixed)              # Command-line game runner
├── Strategy.py                  # Abstract strategy interface
├── RandomStrategy.py            # Random action strategy
├── BasicStrategy.py             # Optimal basic strategy implementation
├── BlackjackGUI.py              # Tkinter-based GUI
├── test_basic_strategy.py       # Unit tests for BasicStrategy
└── test_strategy_comparison.py  # Strategy performance comparison tests

## Installation
### Prerequisites
pip install matplotlib numpy

For GUI (Tkinter usually comes with Python):
* Windows/Mac: Included with Python
* Linux: sudo apt-get install python3-tk

## Usage
1. Run GUI Version (Recommended)
python BlackjackGUI.py

Features:
* Visual card display with suit symbols
* Real-time statistics (wins/losses/draws)
* Hidden dealer card until player finishes
* Action buttons (Hit, Stand, Double Down, )