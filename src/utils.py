"""
Utility functions for displaying and manipulating Sudoku grids.
"""
from typing import List, Optional

class GridFormatter:
    @staticmethod
    def print_grid(grid: Optional[List[List[int]]], title: str = "Sudoku Grid"):
        """Pretty print the Sudoku grid."""
        print(f"\n{title}")
        print("=" * len(title))
        
        if grid is None:
            print("No solution found!")
            return
        
        print("┌─────────┬─────────┬─────────┐")
        for i in range(9):
            if i == 3 or i == 6:
                print("├─────────┼─────────┼─────────┤")
            
            row_str = "│ "
            for j in range(9):
                if j == 3 or j == 6:
                    row_str += "│ "
                
                if grid[i][j] == 0:
                    row_str += ". "
                else:
                    row_str += f"{grid[i][j]} "
            
            row_str += "│"
            print(row_str)
        
        print("└─────────┴─────────┴─────────┘")
    
    @staticmethod
    def grid_to_string(grid: List[List[int]]) -> str:
        """Convert grid to compact string representation."""
        return ''.join(str(cell) for row in grid for cell in row)
    
    @staticmethod
    def string_to_grid(s: str) -> List[List[int]]:
        """Convert string representation back to grid."""
        if len(s) != 81:
            raise ValueError("String must be exactly 81 characters")
        
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                char = s[i * 9 + j]
                row.append(0 if char == '.' or char == '0' else int(char))
            grid.append(row)
        
        return grid