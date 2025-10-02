from typing import List, Tuple, Set

class Ship:
    def __init__(self, cells: List[Tuple[int, int]]):
        self.cells = set(cells)
        self.hits: Set[Tuple[int, int]] = set()
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
