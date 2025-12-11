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
            
    @classmethod
    def from_dimensions(
        cls,
        height: int,
        width: int,
        fill_char: str = '.'
    ) -> 'Grid':
        """Create a grid of given dimensions filled with a character."""
        data = [[fill_char] * width for _ in range(height)]
        return cls(data)
    
    @classmethod
    def from_file(
        cls,
        filepath: str
    ) -> 'Grid':
        """Load a grid from a text file (one row per line)."""
        with open(filepath, 'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
        max_len = max(len(line) for line in lines) if lines else 0
        padded = [line.ljust(max_len) for line in lines]
        return cls(padded)
    
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
    
    def is_inside_polygon(
        self,
        point: Tuple[int, int],
        perimeter: Set[Tuple[int, int]]
    ) -> bool:
        """
        Check if a point is WITHIN a polygon (inside OR on perimeter).
        """
        # On the perimeter = within
        if point in perimeter:
            return True
        
        r, c = point
        crossings = 0
        
        # Cast ray to the right, count perimeter crossings
        for check_c in range(c + 1, self.width):
            if (r, check_c) in perimeter:
                crossings += 1
        
        # Odd crossings = inside, even = outside
        return crossings % 2 == 1

    def is_within_shape(
        self,
        positions: List[Tuple[int, int]],
        shape: Set[Tuple[int, int]],
        shape_is_filled: bool = True,
        positions_is_filled: bool = True
    ) -> bool:
        """
        Check if ALL positions are within the shape.
        
        Args:
            positions: Coordinates to check (can be area or perimeter)
            shape: Shape coordinates (can be area or perimeter)
            shape_is_filled: True if shape contains all interior points, False if perimeter only
            positions_is_filled: True if positions contains all interior points, False if perimeter only
        """
        # Convert to set for O(1) lookup
        shape_set = set(shape) if not isinstance(shape, set) else shape
        
        if shape_is_filled:
            # Shape has all points - simple membership check
            # Works for both filled and perimeter positions
            return all(pos in shape_set for pos in positions)
        else:
            # Shape is perimeter only - need ray casting
            if positions_is_filled:
                # Check every position with ray casting
                return all(self.is_inside_polygon(pos, shape_set) for pos in positions)
            else:
                # Positions is perimeter only - if all perimeter points are inside,
                # the whole rectangle is inside (for convex shapes like rectangles)
                return all(self.is_inside_polygon(pos, shape_set) for pos in positions)
    
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
    # TRACING 
    # ------------------------------------------------
    
    def trace_rectangle(
        self,
        corner1: Tuple[int, int],
        corner2: Tuple[int, int], 
        fill: bool = True
    ) -> List[Tuple[int, int]]:
        """
        Get coordinates of a rectangle.
        
        Args:
            corner1, corner2: Opposite corners of rectangle
            fill: If True, return all interior positions. If False, return perimeter only.
        
        Returns:
            List of (row, col) coordinates
        """
        r1, c1 = corner1
        r2, c2 = corner2
        
        # Ensure r1,c1 is top-left and r2,c2 is bottom-right
        r1, r2 = min(r1, r2), max(r1, r2)
        c1, c2 = min(c1, c2), max(c1, c2)
        
        if fill:
            # All positions inside the rectangle
            positions = [(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]
        else:
            # Perimeter only
            positions = []
            # Top and bottom edges
            for c in range(c1, c2 + 1):
                positions.append((r1, c))
                positions.append((r2, c))
            # Left and right edges (excluding corners already added)
            for r in range(r1 + 1, r2):
                positions.append((r, c1))
                positions.append((r, c2))
        
        return positions
    
    def trace_polygon(
        self,
        corners: List[Tuple[int, int]],
        fill: bool = False
    ) -> Set[Tuple[int, int]]:
        """
        Trace a polygon from ordered corner points.
        
        Args:
            corners: List of (row, col) corners in order
            fill: If False, return perimeter only. If True, return all interior coordinates.
        
        Returns:
            Set of (row, col) coordinates
        """
        # Get perimeter
        perimeter = set()
        for i in range(len(corners)):
            p1 = corners[i]
            p2 = corners[(i + 1) % len(corners)]
            
            r1, c1 = p1
            r2, c2 = p2
            
            if r1 == r2:
                for c in range(min(c1, c2), max(c1, c2) + 1):
                    perimeter.add((r1, c))
            elif c1 == c2:
                for r in range(min(r1, r2), max(r1, r2) + 1):
                    perimeter.add((r, c1))
        
        if not fill:
            return perimeter
        
        # Flood fill from (0, 0) to find outside
        outside = set()
        to_visit = [(0, 0)]
        
        while to_visit:
            r, c = to_visit.pop()
            
            if (r, c) in outside:
                continue
            if not self.in_bounds(r, c):
                continue
            if (r, c) in perimeter:
                continue
            
            outside.add((r, c))
            
            to_visit.append((r - 1, c))
            to_visit.append((r + 1, c))
            to_visit.append((r, c - 1))
            to_visit.append((r, c + 1))
        
        # Inside = all positions - outside
        all_positions = set(self.iter_positions())
        return all_positions - outside
    
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