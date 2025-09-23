# Battleship Game

A Python implementation of the classic Battleship board game, playable in the command line.

## Problem Description

Battleship is a strategy type guessing game for two players. In this single-player version, you play against the computer, which randomly places ships on a hidden 10x10 grid. Your goal is to find and sink all the opponent's ships before running out of turns.

## Features

- 10x10 game board
- Ships of varying sizes: 1x4, 2x3, 3x2, and 4x1
- Clear visual feedback for hits, misses, and sunken ships
- Game statistics (turns taken, hits, ships sunk)
- Ships are placed with at least one cell of space between them

## Setup Instructions

1. **Prerequisites**:
   - Python 3.6 or higher

2. **Installation**:
   ```bash
   # Navigate to the project directory
   cd /path/to/Battleship
   
   # (Optional) Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Running the Game**:
   ```bash
   python Battleship.py
   ```

4. **How to Play**:
   - Enter coordinates in the format `row column` (e.g., `3 5`)
   - The game will show:
     - `X` for hits
     - `O` for misses
     - ` ` (space) for untried cells
   - You'll receive notifications when you sink a ship
   - The game ends when all ships are sunk

## Design Decisions

### Architecture
- **Modular Code**: The game is structured with clear separation of concerns into functions
- **State Management**: The game state is maintained in a clear, consistent manner

### Key Components
1. **Game Board**:
   - 10x10 grid implemented as a 2D list
   - Ships are placed randomly with proper spacing
   - Visual representation adapts to show/hide ships based on context

2. **Ship Management**:
   - Ships are stored as dictionaries containing their cells, hit status, and size
   - Ships can be placed horizontally or vertically
   - Automatic detection of ship sinking

3. **Input/Output**:
   - Simple command-line interface
   - Clear visual feedback
   - Helpful error messages for invalid inputs

### Algorithms
- **Ship Placement**: Uses a recursive algorithm to ensure ships don't touch each other
- **Hit Detection**: Efficiently checks and updates ship status
- **Sinking Detection**: Tracks hits to determine when a ship is fully sunk

## Future Enhancements

1. Add a graphical user interface (GUI)
2. Implement a two-player mode
3. Add different difficulty levels
4. Include sound effects
5. Add a high score system

## License

MIT License

---

Enjoy the game! If you have any questions or suggestions, please feel free to open an issue or submit a pull request.
