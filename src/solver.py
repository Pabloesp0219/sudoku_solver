"""
Enhanced Sudoku Solver with improved algorithms and error handling.
"""
from typing import List, Optional, Tuple, Set
import time
import copy

class SudokuSolver:
    def __init__(self, debug: bool = False, max_backtracks: int = 1000000):
        self.debug = debug
        self.max_backtracks = max_backtracks
        self.solve_time = 0
        self.backtrack_count = 0
        self.constraint_checks = 0
        self.attempts_count = 0
    
    def solve(self, grid: List[List[int]]) -> Optional[List[List[int]]]:
        """
        Main solve method with preprocessing and performance tracking.
        """
        if not self._is_valid_input(grid):
            raise ValueError("Invalid input grid")
        
        start_time = time.time()
        self.backtrack_count = 0
        self.constraint_checks = 0
        self.attempts_count = 0
        
        # Create working copy
        working_grid = copy.deepcopy(grid)
        
        # Enhanced preprocessing: fill obvious cells and apply advanced techniques
        self._preprocess(working_grid)
        
        # Solve using backtracking with early termination
        success = self._solve_recursive(working_grid)
        
        self.solve_time = time.time() - start_time
        
        if self.debug:
            print(f"Solve time: {self.solve_time:.4f}s")
            print(f"Backtracks: {self.backtrack_count}")
            print(f"Attempts: {self.attempts_count}")
            print(f"Constraint checks: {self.constraint_checks}")
        
        return working_grid if success else None
    
    def _is_valid_input(self, grid: List[List[int]]) -> bool:
        """Validate input grid format and constraints."""
        if not grid or len(grid) != 9:
            return False
        
        for row in grid:
            if not row or len(row) != 9:
                return False
            for cell in row:
                if not isinstance(cell, int) or cell < 0 or cell > 9:
                    return False
        
        return self._is_valid_state(grid)
    
    def _is_valid_state(self, grid: List[List[int]]) -> bool:
        """Check if current grid state is valid (no conflicts)."""
        self.constraint_checks += 1
        
        # Check rows
        for row in grid:
            seen = set()
            for cell in row:
                if cell != 0:
                    if cell in seen:
                        return False
                    seen.add(cell)
        
        # Check columns
        for col in range(9):
            seen = set()
            for row in range(9):
                cell = grid[row][col]
                if cell != 0:
                    if cell in seen:
                        return False
                    seen.add(cell)
        
        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                seen = set()
                for row in range(3):
                    for col in range(3):
                        cell = grid[box_row * 3 + row][box_col * 3 + col]
                        if cell != 0:
                            if cell in seen:
                                return False
                            seen.add(cell)
        
        return True
    
    def _preprocess(self, grid: List[List[int]]) -> bool:
        """Enhanced preprocessing: fill cells with only one possible value and apply advanced techniques."""
        changed = True
        iterations = 0
        max_iterations = 10  # Prevent infinite loops
        
        while changed and iterations < max_iterations:
            changed = False
            iterations += 1
            
            # Method 1: Fill cells with only one possible value
            for row in range(9):
                for col in range(9):
                    if grid[row][col] == 0:
                        possible = self._get_possible_values(grid, row, col)
                        if len(possible) == 1:
                            value = next(iter(possible))
                            grid[row][col] = value
                            changed = True
                            if self.debug:
                                print(f"Preprocessing: Set ({row},{col}) = {value}")
            
            # Method 2: Hidden singles (value appears only once in row/col/box)
            if not changed:
                changed = self._apply_hidden_singles(grid)
        
        return True
    
    def _apply_hidden_singles(self, grid: List[List[int]]) -> bool:
        """Apply hidden singles technique."""
        changed = False
        
        # Check rows for hidden singles
        for row in range(9):
            empty_cells = [(row, col) for col in range(9) if grid[row][col] == 0]
            if len(empty_cells) > 1:
                for value in range(1, 10):
                    if value not in grid[row]:  # Value not already in row
                        possible_cells = []
                        for r, c in empty_cells:
                            if value in self._get_possible_values(grid, r, c):
                                possible_cells.append((r, c))
                        
                        if len(possible_cells) == 1:
                            r, c = possible_cells[0]
                            grid[r][c] = value
                            changed = True
                            if self.debug:
                                print(f"Hidden single in row: Set ({r},{c}) = {value}")
        
        # Check columns for hidden singles
        for col in range(9):
            empty_cells = [(row, col) for row in range(9) if grid[row][col] == 0]
            if len(empty_cells) > 1:
                column_values = [grid[row][col] for row in range(9)]
                for value in range(1, 10):
                    if value not in column_values:  # Value not already in column
                        possible_cells = []
                        for r, c in empty_cells:
                            if value in self._get_possible_values(grid, r, c):
                                possible_cells.append((r, c))
                        
                        if len(possible_cells) == 1:
                            r, c = possible_cells[0]
                            grid[r][c] = value
                            changed = True
                            if self.debug:
                                print(f"Hidden single in column: Set ({r},{c}) = {value}")
        
        return changed
    
    def _get_possible_values(self, grid: List[List[int]], row: int, col: int) -> Set[int]:
        """Get all possible values for a cell."""
        if grid[row][col] != 0:
            return set()
        
        used_values = set()
        
        # Check row
        used_values.update(grid[row])
        
        # Check column
        for r in range(9):
            used_values.add(grid[r][col])
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                used_values.add(grid[r][c])
        
        # Remove 0 from used values (it represents empty cells)
        used_values.discard(0)
        
        return {i for i in range(1, 10)} - used_values
    
    def _find_best_cell(self, grid: List[List[int]]) -> Tuple[Optional[Tuple[int, int]], Set[int]]:
        """Find empty cell with minimum possible values (MRV heuristic) with tie-breaking."""
        min_options = 10
        best_cell = None
        best_options = set()
        candidates = []
        
        # Find all cells with minimum remaining values
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    options = self._get_possible_values(grid, row, col)
                    if len(options) < min_options:
                        min_options = len(options)
                        candidates = [(row, col, options)]
                    elif len(options) == min_options:
                        candidates.append((row, col, options))
                        
                        if min_options == 0:
                            return (row, col), options
        
        if not candidates:
            return None, set()
        
        # If multiple candidates with same MRV, use degree heuristic (most constrained)
        if len(candidates) > 1:
            best_candidate = self._apply_degree_heuristic(grid, candidates)
            return best_candidate[0], best_candidate[1]
        
        row, col, best_options = candidates[0]
        best_cell = (row, col)
        return best_cell, best_options
    
    def _apply_degree_heuristic(self, grid: List[List[int]], candidates: List[Tuple[int, int, Set[int]]]) -> Tuple[Tuple[int, int], Set[int]]:
        """Apply degree heuristic: choose cell that constrains most other cells."""
        max_constraints = -1
        best_candidate = candidates[0]
        
        for row, col, options in candidates:
            constraints = 0
            # Count empty cells in same row, column, and box
            for r in range(9):
                if r != row and grid[r][col] == 0:
                    constraints += 1
            for c in range(9):
                if c != col and grid[row][c] == 0:
                    constraints += 1
            
            # Count empty cells in same 3x3 box
            box_row, box_col = 3 * (row // 3), 3 * (col // 3)
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    if (r != row or c != col) and grid[r][c] == 0:
                        constraints += 1
            
            if constraints > max_constraints:
                max_constraints = constraints
                best_candidate = (row, col, options)
        
        return (best_candidate[0], best_candidate[1]), best_candidate[2]
    
    def _solve_recursive(self, grid: List[List[int]]) -> bool:
        """Recursive backtracking solver with MRV heuristic and constraint validation."""
        # Early termination check
        if self.backtrack_count >= self.max_backtracks:
            if self.debug:
                print(f"Early termination: exceeded {self.max_backtracks} backtracks")
            return False
        
        cell, options = self._find_best_cell(grid)
        
        if cell is None:
            return True  # Solved!
        
        if not options:
            return False  # No valid options, backtrack
        
        row, col = cell
        
        # Try each possible value with improved ordering
        for value in self._get_ordered_values(options, grid, row, col):
            grid[row][col] = value
            self.attempts_count += 1
            
            # Validate constraints after placing the value
            if self._is_valid_state(grid):
                if self.debug and self.attempts_count % 10000 == 0:
                    print(f"Attempts: {self.attempts_count}, Backtracks: {self.backtrack_count}")
                
                if self._solve_recursive(grid):
                    return True
                
                # This was a backtrack
                self.backtrack_count += 1
            
            # Backtrack
            grid[row][col] = 0
        
        return False
    
    def _get_ordered_values(self, options: Set[int], grid: List[List[int]], row: int, col: int) -> List[int]:
        """Get values ordered by least constraining value heuristic."""
        # For minimal puzzles, try values that appear least frequently in the puzzle
        value_counts = {}
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                if val != 0:
                    value_counts[val] = value_counts.get(val, 0) + 1
        
        # Sort by frequency (ascending) - try least frequent values first
        sorted_options = sorted(options, key=lambda x: value_counts.get(x, 0))
        return sorted_options
    
    def get_stats(self) -> dict:
        """Return solving statistics."""
        return {
            'solve_time': self.solve_time,
            'backtrack_count': self.backtrack_count,
            'attempts_count': self.attempts_count,
            'constraint_checks': self.constraint_checks
        }