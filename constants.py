# Game board constants
BOARD_SIZE = 10
EMPTY_CELL = ' '
SHIP_CELL = 'S'
HIT_MARKER = 'X'
MISS_MARKER = 'O'

# Ship configuration
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Ship sizes: 1x4, 2x3, 3x2, 4x1

# Game messages
WELCOME_MSG = "Welcome to Battleship!"
TRY_TO_SINK = "Try to sink all ships!"
HIT_MSG = "\nHIT!"
MISS_MSG = "\nMISS!"
GAME_OVER_MSG = "\n=== GAME OVER! ==="
SHIP_SUNK_MSG = "\n=== YOU SUNK A {}-CELL SHIP! ===\n"

# Input prompts
ENTER_COORDS_PROMPT = "Enter row and column (0-{}), separated by space: "
INVALID_COORDS_MSG = "Please enter exactly two numbers separated by a space."
COORDS_RANGE_MSG = "Coordinates must be between 0 and {}."
ALREADY_TRIED_MSG = "You've already tried that position."
INVALID_NUMBER_MSG = "Please enter valid numbers."

# Error messages
SHIP_PLACEMENT_ERROR = "Failed to place ship of size {} after {} attempts"
