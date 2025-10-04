"""
Sudoku puzzle validator and utility functions.
"""
from typing import List

class SudokuValidator:
    @staticmethod
    def is_complete(grid: List[List[int]]) -> bool:
        """Check if puzzle is completely filled."""
        for row in grid:
            for cell in row:
                if cell == 0:
                    return False
        return True
    
    @staticmethod
    def is_valid_solution(grid: List[List[int]]) -> bool:
        """Check if completed grid is a valid solution."""
        if not SudokuValidator.is_complete(grid):
            return False
        
        # Check all constraints
        return SudokuValidator._check_constraints(grid)
    
    @staticmethod
    def _check_constraints(grid: List[List[int]]) -> bool:
        """Check all Sudoku constraints."""
        # Check rows
        for row in grid:
            if sorted(row) != list(range(1, 10)):
                return False
        
        # Check columns
        for col in range(9):
            column = [grid[row][col] for row in range(9)]
            if sorted(column) != list(range(1, 10)):
                return False
        
        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for row in range(3):
                    for col in range(3):
                        box.append(grid[box_row * 3 + row][box_col * 3 + col])
                if sorted(box) != list(range(1, 10)):
                    return False
        
        return True
    
    @staticmethod
    def count_clues(grid: List[List[int]]) -> int:
        """Count number of given clues in puzzle."""
        return sum(1 for row in grid for cell in row if cell != 0)