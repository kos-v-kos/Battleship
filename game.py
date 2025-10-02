import random
from typing import List, Tuple, Optional
from constants import (
    SHIP_SIZES, BOARD_SIZE, WELCOME_MSG, TRY_TO_SINK, HIT_MSG, MISS_MSG,
    GAME_OVER_MSG, SHIP_SUNK_MSG, ENTER_COORDS_PROMPT, INVALID_COORDS_MSG,
    COORDS_RANGE_MSG, ALREADY_TRIED_MSG, INVALID_NUMBER_MSG, SHIP_PLACEMENT_ERROR
)
from models.board import Board
from models.ship import Ship

class Game:
    SHIP_SIZES = SHIP_SIZES  # Ship sizes: 1x4, 2x3, 3x2, 4x1
    
    def __init__(self, board_size: int = BOARD_SIZE):
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

    def get_player_move(self) -> Tuple[int, int]:
        """Get valid coordinates from the player."""
        while True:
            try:
                coords = input(ENTER_COORDS_PROMPT.format(self.board.size - 1)).strip().split()
                if len(coords) != 2:
                    print(INVALID_COORDS_MSG)
                    continue

                x, y = map(int, coords)
                if not (0 <= x < self.board.size and 0 <= y < self.board.size):
                    print(COORDS_RANGE_MSG.format(self.board.size - 1))
                    continue

                if (x, y) in self.board.hits or (x, y) in self.board.misses:
                    print(ALREADY_TRIED_MSG)
                    continue

                return x, y
            except ValueError:
                print(INVALID_NUMBER_MSG)
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

    def play(self) -> None:
        """Main game loop."""
        print(WELCOME_MSG)
        print(TRY_TO_SINK)
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
                print(HIT_MSG)
                if sunk_size:
                    self.ships_sunk += 1
                    print(SHIP_SUNK_MSG.format(sunk_size))
                    
                    # Show remaining ships
                    remaining = [s for s in self.SHIP_SIZES 
                               if s not in [ship.size for ship in self.board.ships if ship.sunk]]
                    if remaining:
                        print(f"Ships remaining: {sorted(remaining, reverse=True)}")
                    print("-" * 40)
            else:
                print(MISS_MSG)

            hits = len(self.board.hits)
            print(f"Hits: {hits}/{self.total_ship_cells}")
            print(f"Ships sunk: {self.ships_sunk}/{len(self.SHIP_SIZES)}")

        print(GAME_OVER_MSG)
        print(f"You sank all {len(self.SHIP_SIZES)} ships in {self.turns} turns!")
        print("\nFinal board:")
        self.board.display(show_ships=True)
