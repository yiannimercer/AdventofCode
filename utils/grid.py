# utils/grid.py

from enum import Enum
from typing import Optional, List, Tuple, Dict, Set, Iterator, Union
from dataclasses import dataclass
from collections import Counter
import copy


class Direction(Enum):
    """Cardinal and diagonal directions with their (row_delta, col_delta) offsets."""
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (-1, 1)
    DOWN_LEFT = (1, -1)
    DOWN_RIGHT = (1, 1)
    
    @property
    def delta(self) -> Tuple[int, int]:
        return self.value
    
    @property
    def opposite(self) -> 'Direction':
        """Return the opposite direction."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.UP_LEFT: Direction.DOWN_RIGHT,
            Direction.DOWN_RIGHT: Direction.UP_LEFT,
            Direction.UP_RIGHT: Direction.DOWN_LEFT,
            Direction.DOWN_LEFT: Direction.UP_RIGHT,
        }
        return opposites[self]
    
    @classmethod
    def cardinals(cls) -> List['Direction']:
        """Return only cardinal directions (up, down, left, right)."""
        return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]
    
    @classmethod
    def diagonals(cls) -> List['Direction']:
        """Return only diagonal directions."""
        return [cls.UP_LEFT, cls.UP_RIGHT, cls.DOWN_LEFT, cls.DOWN_RIGHT]
    
    @classmethod
    def all(cls) -> List['Direction']:
        """Return all 8 directions."""
        return list(cls)


@dataclass
class Cell:
    """Represents a cell in the grid with its position and value."""
    row: int
    col: int
    value: str
    
    @property
    def pos(self) -> Tuple[int, int]:
        return (self.row, self.col)
    
    def __repr__(self):
        return f"Cell({self.row}, {self.col}, '{self.value}')"


class Grid:
    """
    A 2D grid class for working with character-based grids.
    
    Coordinates use (row, col) where (0, 0) is the top-left corner.
    Row increases downward, column increases rightward.
    """
    
    def __init__(
        self,
        data: Union[List[str], List[List[str]]]
    ):
        """
        Initialize grid from a list of strings or list of lists.
        
        Args:
            data: List of equal-length strings, or list of lists of single characters
        """
        if not data:
            raise ValueError("Grid cannot be empty")
        
        # Convert to list of lists for mutability
        if isinstance(data[0], str):
            self._grid: List[List[str]] = [list(row) for row in data]
        else:
            self._grid = [list(row) for row in data]
        
        # Validate all rows have same length
        self._height = len(self._grid)
        self._width = len(self._grid[0]) if self._grid else 0
        
        for i, row in enumerate(self._grid):
            if len(row) != self._width:
                raise ValueError(f"Row {i} has length {len(row)}, expected {self._width}")
            
            
    # ------------------------------------------------
    # PROPERTIES 
    # ------------------------------------------------
    
    @property
    def height(
        self
    ) -> int:
        """Number of rows in the grid."""
        return self._height
    
    @property
    def width(
        self
    ) -> int:
        """Number of columns in the grid."""
        return self._width
    
    @property
    def size(
        self
    ) -> Tuple[int, int]:
        """Return (height, width) tuple."""
        return (self._height, self._width)
    
    @property
    def area(
        self
    ) -> int:
        """Return total number of cells in the grid."""
        return self._height * self._width
    
    # ------------------------------------------------
    # BASIC ACCESS 
    # ------------------------------------------------
    
    def in_bounds(
        self,
        row: int,
        col: int
    ) -> bool:
        """Check if a position is within the grid boundaries."""
        return 0 <= row < self._height and 0 <= col < self._width
    
    def get(
        self,
        row: int,
        col: int,
        default: Optional[str] = None
    ) -> Optional[str]:
        """
        Get value at position, returning default if out of bounds.
        
        Args:
            row: Row index
            col: Column index
            default: Value to return if out of bounds (default: None)
        """
        if self.in_bounds(row, col):
            return self._grid[row][col]
        return default
    
    def get_row(self, row: int) -> Optional[List[str]]:
        """Get a copy of a row as a list."""
        if 0 <= row < self._height:
            return self._grid[row].copy()
        return None

    def get_col(self, col: int) -> Optional[List[str]]:
        """Get a column as a list."""
        if 0 <= col < self._width:
            return [self._grid[row][col] for row in range(self._height)]
        return None
    
    def set(
        self,
        row: int,
        col: int,
        value: str
    ) -> bool:
        """
        Set value at position. Returns True if successful, False if out of bounds.
        """
        if self.in_bounds(row, col):
            self._grid[row][col] = value
            return True
        return False
    
    def set_positions(
        self,
        positions: Union[Tuple[int, int], List[Tuple[int, int]]],
        value: str
    ) -> int:
        """
        Set value at one or more positions. Return the count of successfully updating positions
        """
        # Handle single tuple
        if isinstance(positions, tuple) and len(positions) == 2 and isinstance(positions[0], int):
            positions = [positions]

        count = 0
        for row, col in positions:
            if self.set(row, col, value):
                count += 1
        return count
    
    def __getitem__(
        self,
        key: Tuple[int, int]
    ) -> Optional[str]:
        """Allow grid[row, col] syntax."""
        row, col = key
        return self.get(row, col)
    
    def __setitem__(
        self,
        key: Tuple[int, int],
        value: str
    ):
        """Allow grid[row, col] = value syntax."""
        row, col = key
        if not self.set(row, col, value):
            raise IndexError(f"Position ({row}, {col}) is out of bounds")
        
    # ------------------------------------------------
    # NAVIGATION 
    # ------------------------------------------------
    
    def move(
        self,
        row: int,
        col: int,
        direction: Direction,
        steps: int = 1
    ) -> Tuple[int, int]:
        """
        Calculate new position after moving in a direction.
        
        Returns the new (row, col) position (may be out of bounds).
        """
        dr, dc = direction.delta
        return (row + dr * steps, col + dc * steps)
    
    def move_if_valid(
        self,
        row: int,
        col: int,
        direction: Direction,
        steps: int = 1
    ) -> Optional[Tuple[int, int]]:
        """
        Move in a direction, returning None if the result is out of bounds.
        """
        new_pos = self.move(row, col, direction, steps)
        if self.in_bounds(*new_pos):
            return new_pos
        return None
    
    def get_in_direction(
        self,
        row: int,
        col: int,
        direction: Direction,
        steps: int = 1,
        default: Optional[str] = None
    ) -> Optional[str]:
        """
        Get the value in a specific direction from a position.
        
        Args:
            row, col: Starting position
            direction: Direction to look
            steps: How many steps in that direction (default: 1)
            default: Value to return if out of bounds
        """
        new_row, new_col = self.move(row, col, direction, steps)
        return self.get(new_row, new_col, default)
    
    # ------------------------------------------------
    # NEIGHBORS / ADJACENT 
    # ------------------------------------------------
    
    def neighbors(
        self,
        row: int,
        col: int, 
        directions: Optional[List[Direction]] = None,
        include_out_of_bounds: bool = False
    ) -> List[Cell]:
        """
        Get all adjacent cells around a position.
        
        Args:
            row, col: Center position
            directions: Which directions to check (default: all 8)
            include_out_of_bounds: If True, include None values for out-of-bounds positions
            
        Returns:
            List of Cell objects for valid neighbors
        """
        if directions is None:
            directions = Direction.all()
        
        result = []
        for direction in directions:
            new_row, new_col = self.move(row, col, direction)
            if self.in_bounds(new_row, new_col):
                result.append(Cell(new_row, new_col, self._grid[new_row][new_col]))
            elif include_out_of_bounds:
                result.append(Cell(new_row, new_col, 'OOB'))
    
        return result
    
    def near(
        self,
        row: int,
        col: int, 
        directions: Optional[List[Direction]] = None
    ) -> Dict[Direction, Optional[Cell]]:
        """
        Get a dictionary mapping directions to adjacent cells.
        
        More structured version of neighbors() that preserves direction information.
        """
        if directions is None:
            directions = Direction.all()
        
        result = {}
        for direction in directions:
            new_row, new_col = self.move(row, col, direction)
            if self.in_bounds(new_row, new_col):
                result[direction] = Cell(new_row, new_col, self._grid[new_row][new_col])
            else:
                result[direction] = None
        
        return result
    
    def cardinal_neighbors(
        self,
        row: int,
        col: int
    ) -> List[Cell]:
        """Get only up/down/left/right neighbors."""
        return self.neighbors(row, col, Direction.cardinals())
    
    def diagonal_neighbors(
        self,
        row: int,
        col: int
    ) -> List[Cell]:
        """Get only diagonal neighbors."""
        return self.neighbors(row, col, Direction.diagonals())
    
    # ------------------------------------------------
    # COUNTING & FINDING 
    # ------------------------------------------------
    
    def col_values(self, col: int) -> Optional[str]:
        """Get all values in a column as a string."""
        if 0 <= col < self._width:
            return "".join(self._grid[row][col] for row in range(self._height))
        return None
    
    def count(
        self,
        char: str
    ) -> int:
        """Count occurrences of a character in the grid."""
        total = 0
        for row in self._grid:
            total += row.count(char)
        return total
    
    def count_all(
        self
    ) -> Counter:
        """Return a Counter of all characters in the grid."""
        counter = Counter()
        for row in self._grid:
            counter.update(row)
        return counter
    
    def count_near(
        self,
        row: int,
        col: int,
        char: str, 
        directions: Optional[List[Direction]] = None
    ) -> int:
        """Count how many neighbors have a specific value."""
        near = self.near(row, col, directions)
        return sum(1 for cell in near.values() if cell and cell.value == char)
    
    def find_all(
        self,
        char: str
    ) -> List[Tuple[int, int]]:
        """Find all positions of a character."""
        positions = []
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == char:
                    positions.append((row, col))
        return positions
    
    def find_first(
        self,
        char: str
    ) -> Optional[Tuple[int, int]]:
        """Find the first occurrence of a character (top-to-bottom, left-to-right)."""
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == char:
                    return (row, col)
        return None
    
    def contains(
        self,
        char: str
    ) -> bool:
        """Check if a character exists in the grid."""
        return self.find_first(char) is not None
    
    def draw(self, 
             show_coords: bool = False,
             highlight: Optional[Set[Tuple[int, int]]] = None,
             highlight_char: str = '*',
             path: Optional[List[Tuple[int, int]]] = None,
             path_char: str = '#') -> str:
        """
        Create a pretty string representation of the grid.
        
        Args:
            show_coords: Show row/column numbers
            highlight: Set of positions to highlight
            highlight_char: Character to use for highlighting (replaces original)
            path: List of positions to show as a path
            path_char: Character to use for path positions
        """
        highlight = highlight or set()
        path_set = set(path) if path else set()
        
        lines = []
        
        # Column headers
        if show_coords:
            if self._width <= 10:
                header = "   " + "".join(str(i) for i in range(self._width))
            else:
                header = "   " + "".join(str(i % 10) for i in range(self._width))
            lines.append(header)
            lines.append("   " + "-" * self._width)
        
        for row in range(self._height):
            row_chars = []
            for col in range(self._width):
                if (row, col) in path_set:
                    row_chars.append(path_char)
                elif (row, col) in highlight:
                    row_chars.append(highlight_char)
                else:
                    row_chars.append(self._grid[row][col])
            
            if show_coords:
                lines.append(f"{row:2}|{''.join(row_chars)}")
            else:
                lines.append("".join(row_chars))
        
        return "\n".join(lines)
    
    # ------------------------------------------------
    # ITERATION ACROSS GRID 
    # ------------------------------------------------
    
    def iter_cells(self) -> Iterator[Cell]:
        """Iterate over all cells in the grid (row by row)."""
        for row in range(self._height):
            for col in range(self._width):
                yield Cell(row, col, self._grid[row][col])
    
    def iter_row(self, row: int) -> Iterator[Cell]:
        """Iterate over cells in a specific row."""
        if 0 <= row < self._height:
            for col in range(self._width):
                yield Cell(row, col, self._grid[row][col])
    
    def iter_col(self, col: int) -> Iterator[Cell]:
        """Iterate over cells in a specific column."""
        if 0 <= col < self._width:
            for row in range(self._height):
                yield Cell(row, col, self._grid[row][col])
    
    def iter_positions(self) -> Iterator[Tuple[int, int]]:
        """Iterate over all (row, col) positions."""
        for row in range(self._height):
            for col in range(self._width):
                yield (row, col)