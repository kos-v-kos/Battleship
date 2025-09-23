import random
from typing import List, Tuple, Optional


class Ship:
    def __init__(self, cells: List[Tuple[int, int]]):
        self.cells = set(cells)
        self.hits = set()
        self.size = len(cells)
        self.sunk = False

    def hit(self, x: int, y: int) -> bool:
        """Register a hit on the ship. Returns True if the ship is sunk."""
        if (x, y) in self.cells:
            self.hits.add((x, y))
            if len(self.hits) == self.size:
                self.sunk = True
                return True
        return False

    def is_at(self, x: int, y: int) -> bool:
        """Check if the ship is at the given coordinates."""
        return (x, y) in self.cells


class Board:
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        self.hits = set()
        self.misses = set()

    def place_ship(self, ship: Ship) -> bool:
        """Place a ship on the board if it fits."""
        # Check if ship can be placed
        for x, y in ship.cells:
            if not (0 <= x < self.size and 0 <= y < self.size):
                return False
            if self.grid[x][y] == 'S':
                return False
            # Check adjacent cells
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.size and 0 <= ny < self.size and 
                            self.grid[nx][ny] == 'S'):
                        return False
        
        # Place the ship
        for x, y in ship.cells:
            self.grid[x][y] = 'S'
        self.ships.append(ship)
        return True

    def attack(self, x: int, y: int) -> Tuple[bool, Optional[int]]:
        """Attack the specified cell. Returns (hit, ship_size) if a ship was sunk."""
        if (x, y) in self.hits or (x, y) in self.misses:
            return False, None

        for ship in self.ships:
            if ship.is_at(x, y):
                self.hits.add((x, y))
                if ship.hit(x, y):  # Check if this hit sunk the ship
                    return True, ship.size
                return True, None
        
        self.misses.add((x, y))
        return False, None

    def is_game_over(self) -> bool:
        """Check if all ships are sunk."""
        return all(ship.sunk for ship in self.ships)

    def display(self, show_ships: bool = False) -> None:
        """Print the current state of the board."""
        print("   " + " ".join(str(i) for i in range(self.size)))
        print("  " + "-" * (2 * self.size + 1))
        for i in range(self.size):
            row = [str(i) + "|"]
            for j in range(self.size):
                if (i, j) in self.hits:
                    row.append('X')
                elif (i, j) in self.misses:
                    row.append('O')
                elif show_ships and self.grid[i][j] == 'S':
                    row.append('S')
                else:
                    row.append(' ')
            print(" ".join(row))


class Game:
    SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Ship sizes: 1x4, 2x3, 3x2, 4x1
    
    def __init__(self, board_size: int = 10):
        self.board = Board(board_size)
        self.turns = 0
        self.ships_sunk = 0
        self.total_ship_cells = sum(self.SHIP_SIZES)
        self.setup_game()

    def setup_game(self) -> None:
        """Set up the game board with ships."""
        for size in sorted(self.SHIP_SIZES, reverse=True):
            self.place_ship(size)

    def place_ship(self, size: int, max_attempts: int = 100) -> None:
        """Place a ship of given size on the board."""
        for _ in range(max_attempts):
            is_horizontal = random.choice([True, False])
            if is_horizontal:
                x = random.randint(0, self.board.size - 1)
                y = random.randint(0, self.board.size - size)
                cells = [(x, y + i) for i in range(size)]
            else:
                x = random.randint(0, self.board.size - size)
                y = random.randint(0, self.board.size - 1)
                cells = [(x + i, y) for i in range(size)]
            
            ship = Ship(cells)
            if self.board.place_ship(ship):
                return
        
        raise RuntimeError(f"Failed to place ship of size {size} after {max_attempts} attempts")

    def get_player_move(self) -> Tuple[int, int] | None:
        """Get valid coordinates from the player."""
        while True:
            try:
                coords = input(f"Enter row and column (0-{self.board.size - 1}), separated by space: ").strip().split()
                if len(coords) != 2:
                    print("Please enter exactly two numbers separated by a space.")
                    continue

                x, y = map(int, coords)
                if not (0 <= x < self.board.size and 0 <= y < self.board.size):
                    print(f"Coordinates must be between 0 and {self.board.size - 1}.")
                    continue

                if (x, y) in self.board.hits or (x, y) in self.board.misses:
                    print("You've already tried that position.")
                    continue

                return x, y  # This is the only return that matches the type hint
            except ValueError:
                print("Please enter valid numbers.")
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

    def play(self) -> None:
        """Main game loop."""
        print("Welcome to Battleship!")
        print("Try to sink all ships!")
        print(f"Ships: {self.SHIP_SIZES.count(4)}x4, {self.SHIP_SIZES.count(3)}x3, "
              f"{self.SHIP_SIZES.count(2)}x2, {self.SHIP_SIZES.count(1)}x1\n")

        # Debug: Show initial board with ships
        print("Initial board with ships (for debugging):")
        self.board.display(show_ships=True)

        print("\nStarting game!")

        while not self.board.is_game_over():
            print(f"\nTurn {self.turns + 1}")
            self.board.display()
            
            print("\nMake your move:")
            x, y = self.get_player_move()

            hit, sunk_size = self.board.attack(x, y)
            self.turns += 1

            if hit:
                print("\nHIT!")
                if sunk_size:
                    self.ships_sunk += 1
                    print(f"\n=== YOU SUNK A {sunk_size}-CELL SHIP! ===\n")
                    
                    # Show remaining ships
                    remaining = [s for s in self.SHIP_SIZES 
                               if s not in [ship.size for ship in self.board.ships if ship.sunk]]
                    if remaining:
                        print(f"Ships remaining: {sorted(remaining, reverse=True)}")
                    print("-" * 40)
            else:
                print("\nMISS!")

            hits = len(self.board.hits)
            print(f"Hits: {hits}/{self.total_ship_cells}")
            print(f"Ships sunk: {self.ships_sunk}/{len(self.SHIP_SIZES)}")

        print("\n=== GAME OVER! ===")
        print(f"You sank all {len(self.SHIP_SIZES)} ships in {self.turns} turns!")
        print("\nFinal board:")
        self.board.display(show_ships=True)


def main():
    """Initialize and start the game."""
    game = Game()
    game.play()


if __name__ == "__main__":
    main()