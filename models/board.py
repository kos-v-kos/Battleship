from typing import List, Tuple, Optional, Set
from ..constants import EMPTY_CELL, SHIP_CELL, HIT_MARKER, MISS_MARKER, BOARD_SIZE
from .ship import Ship

class Board:
    def __init__(self, size: int = BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY_CELL for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        self.hits: Set[Tuple[int, int]] = set()
        self.misses: Set[Tuple[int, int]] = set()

    def place_ship(self, ship: Ship) -> bool:
        """Place a ship on the board if it fits."""
        # Check if ship can be placed
        for x, y in ship.cells:
            if not (0 <= x < self.size and 0 <= y < self.size):
                return False
            if self.grid[x][y] == SHIP_CELL:
                return False
            # Check adjacent cells
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.size and 0 <= ny < self.size and 
                            self.grid[nx][ny] == SHIP_CELL):
                        return False
        
        # Place the ship
        for x, y in ship.cells:
            self.grid[x][y] = SHIP_CELL
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
                    row.append(HIT_MARKER)
                elif (i, j) in self.misses:
                    row.append(MISS_MARKER)
                elif show_ships and self.grid[i][j] == SHIP_CELL:
                    row.append(SHIP_CELL)
                else:
                    row.append(EMPTY_CELL)
            print(" ".join(row))
