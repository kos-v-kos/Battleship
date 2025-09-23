# Battleship Game

A Python implementation of the classic Battleship board game, now with an object-oriented design, playable in the command line.

## Problem Description

Battleship is a strategy type guessing game for two players. In this single-player version, you play against the computer, which randomly places ships on a hidden 10x10 grid. Your goal is to find and sink all the opponent's ships in as few turns as possible.

## Features

- 🚢 10x10 game board with a clean command-line interface
- ⚓ Ships of varying sizes: 
  - 1x 4-cell ship
  - 2x 3-cell ships
  - 3x 2-cell ships
  - 4x 1-cell ships
- 🎯 Clear visual feedback for hits (`X`), misses (`O`), and sunken ships
- 📊 Game statistics (turns taken, hits, ships sunk)
- 🛡️ Ships are placed with at least one cell of space between them
- 🔍 Debug mode to show ship positions (for testing)

## Setup Instructions

1. **Prerequisites**:
   - Python 3.6 or higher

2. **Installation**:
   ```bash
   # Clone the repository (if applicable)
   # git clone [repository-url]
   
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
   - You'll receive notifications when you sink a ship, including the ship size
   - The game ends when all ships are sunk

## Object-Oriented Design

The game is built using a clean, object-oriented architecture with three main classes:

### 1. `Ship` Class
- Manages individual ship state and behavior
- Tracks ship position, hits, and sinking status
- Provides methods for checking if a ship is at specific coordinates

### 2. `Board` Class
- Manages the 10x10 game grid
- Handles ship placement with proper spacing
- Tracks hits, misses, and game state
- Provides methods for displaying the board

### 3. `Game` Class
- Manages the overall game flow
- Handles player input and turn management
- Tracks game statistics and win conditions
- Provides feedback and game state information

### Key Algorithms
- **Ship Placement**: Random placement with collision detection
- **Hit Detection**: Efficient coordinate checking against ship positions
- **Sinking Detection**: Tracks hits to determine when a ship is fully sunk
- **Input Validation**: Ensures valid moves and provides helpful error messages

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
