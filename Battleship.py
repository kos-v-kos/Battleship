import random

BOARD_SIZE = 10
SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Ship sizes: 1x4, 2x3, 3x2, 4x1


def setup_game():
    """Initialize the game board and place ships."""
    while True:
        board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        ships_placed = place_ships([row[:] for row in board])
        if ships_placed is None:
            continue
            
        # Create ship objects with their positions and hit status
        ships = []
        temp_ships = ships_placed.copy()
        
        # Place ships on the board
        for x, y in ships_placed:
            board[x][y] = 'S'
            
        # Group ship cells
        temp_ships = ships_placed.copy()
        while temp_ships:
            start_x, start_y = temp_ships.pop()
            ship_cells = [(start_x, start_y)]
            
            # Find all connected cells (same ship)
            queue = [(start_x, start_y)]
            while queue:
                x, y = queue.pop(0)
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in temp_ships:
                        ship_cells.append((nx, ny))
                        temp_ships.remove((nx, ny))
                        queue.append((nx, ny))
            
            # Create ship object
            ships.append({
                'cells': ship_cells,
                'hits': set(),
                'size': len(ship_cells),
                'sunk': False
            })
            
        return board, ships


def is_valid_cell(x, y):
    """Check if cell coordinates are within board boundaries."""
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def can_place_ship(board, x, y, size, is_horizontal):
    """Check if a ship can be placed at the given position without touching other ships."""
    # Check all cells where the ship will be placed and their neighbors
    for i in range(-1, size + 1):
        for j in range(-1, 2):  # Check one cell above, same level, and one below
            if is_horizontal:
                check_x, check_y = x + j, y + i
            else:
                check_x, check_y = x + i, y + j
            
            if is_valid_cell(check_x, check_y):
                # If it's part of the ship, it should be empty
                if (is_horizontal and 0 <= i < size and j == 0) or \
                   (not is_horizontal and 0 <= i < size and j == 0):
                    if board[check_x][check_y] != ' ':
                        return False
                # If it's adjacent to the ship, it should be empty
                elif board[check_x][check_y] == 'S':
                    return False
    
    # Check the ship fits within the board
    if is_horizontal:
        if y + size > BOARD_SIZE:
            return False
    else:
        if x + size > BOARD_SIZE:
            return False
            
    return True


def place_ship(board, size, max_attempts=100):
    """Place a single ship of given size on the board with no adjacent ships."""
    attempts = 0
    while attempts < max_attempts:
        is_horizontal = random.choice([True, False])
        if is_horizontal:
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - size)
        else:
            x = random.randint(0, BOARD_SIZE - size)
            y = random.randint(0, BOARD_SIZE - 1)

        if can_place_ship(board, x, y, size, is_horizontal):
            ship_cells = []
            for i in range(size):
                if is_horizontal:
                    board[x][y + i] = 'S'
                    ship_cells.append((x, y + i))
                else:
                    board[x + i][y] = 'S'
                    ship_cells.append((x + i, y))
            return ship_cells
        attempts += 1
    
    # If we couldn't place the ship after max_attempts, return None
    return None


def place_ships(board):
    """Place all ships on the board with no ships touching each other."""
    ships = []
    # Sort ships by size (largest first) to make placement easier
    for size in sorted(SHIPS, reverse=True):
        ship_cells = place_ship(board, size)
        if ship_cells is None:
            # If we couldn't place a ship, return None to indicate failure
            return None
        ships.extend(ship_cells)
    return ships


def print_board(board, show_ships=False):
    """Print the game board. If show_ships is False, hides the ships."""
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for i in range(BOARD_SIZE):
        row = [str(i)]
        for j in range(BOARD_SIZE):
            cell = board[i][j]
            if not show_ships and cell == 'S':
                row.append(' ')
            else:
                row.append(cell)
        print(" ".join(row))


def get_player_move():
    """Get valid coordinates from the player in format 'row column'."""
    while True:
        try:
            coords = input(f"Enter row and column (0-{BOARD_SIZE - 1}), separated by space: ").split()
            if len(coords) != 2:
                print("Please enter exactly two numbers separated by a space.")
                continue
                
            x, y = map(int, coords)
            
            if not (0 <= x < BOARD_SIZE) or not (0 <= y < BOARD_SIZE):
                print(f"Both coordinates must be between 0 and {BOARD_SIZE - 1}. Try again.")
                continue
                
            return x, y
            
        except ValueError:
            print("Please enter two numbers separated by a space (e.g., '3 4').")


def check_sunk_ships(board, ships, hit_cells):
    """Check if any ships have been sunk and return a list of sunken ship sizes."""
    sunk_ships = []
    for ship in ships:
        if ship['sunk']:
            continue
            
        # Update hits for this ship
        ship['hits'] = {(x, y) for x, y in ship['cells'] if (x, y) in hit_cells}
        
        # Check if all cells are hit
        if len(ship['hits']) == len(ship['cells']):
            ship['sunk'] = True
            sunk_ships.append(len(ship['cells']))
            
            # Mark all cells as hit on the board
            for x, y in ship['cells']:
                board[x][y] = 'X'
                
    return sunk_ships

def play_game():
    """Main game loop."""
    print("Welcome to Battleship!")
    print("Try to sink all ships!")
    print("Ships: 1x4, 2x3, 3x2, 4x1")

    board, ships = setup_game()
    print("\nInitial board with ships (for debugging):")
    print_board(board, True)
    print("\nStarting game!")
    
    turns = 0
    total_ship_cells = sum(ship['size'] for ship in ships)
    hit_cells = set()  # Track all hit cells
    sunk_ships_count = 0  # Count of sunk ships
    
    # Debug: Print ship info
    print("\nShip information (for debugging):")
    for i, ship in enumerate(ships, 1):
        print(f"Ship {i}: size={ship['size']}, cells={ship['cells']}")
    print()

    while True:
        # Check if all ships are sunk
        if all(ship['sunk'] for ship in ships):
            break
            
        print(f"\nTurn {turns + 1}")
        print("   " + " ".join(str(i) for i in range(BOARD_SIZE)))  # Column numbers
        print("  " + "-" * (2 * BOARD_SIZE + 1))
        
        # Display the board (hiding unsunk ships)
        print_board(board, show_ships=False)

        print("\nMake your move:")
        x, y = get_player_move()

        if (x, y) in hit_cells:
            print("You already tried that spot!")
            continue

        hit_cells.add((x, y))
        
        if board[x][y] == 'S':
            print("\nHIT!")
            board[x][y] = 'X'
            
            # Check for sunk ships
            sunk_ship_sizes = check_sunk_ships(board, ships, hit_cells)
            
            # Check if any new ships were sunk
            for ship in ships:
                if ship['sunk'] and len(ship['hits']) == ship['size']:
                    print(f"\n=== YOU SUNK A {ship['size']}-CELL SHIP! ===\n")
                    sunk_ships_count += 1
                    
                    # Show remaining ships
                    remaining = [s['size'] for s in ships if not s['sunk']]
                    if remaining:
                        print(f"Ships remaining: {sorted(remaining, reverse=True)}")
                    print("-" * 40)
                    
        else:
            print("\nMISS!")
            board[x][y] = 'O'

        turns += 1
        hits = len([cell for cell in hit_cells if board[cell[0]][cell[1]] == 'X'])
        print(f"Hits: {hits}/{total_ship_cells}")
        print(f"Ships sunk: {sunk_ships_count}/{len(ships)}")

    print(f"\n=== GAME OVER! ===")
    print(f"You sank all {len(ships)} ships in {turns} turns!")
    print("\nFinal board:")
    print_board(board, show_ships=True)


if __name__ == "__main__":
    play_game()