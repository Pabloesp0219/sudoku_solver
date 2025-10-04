"""
Comprehensive test suite for the Sudoku solver.
"""
import unittest
import sys
import os

# Fix import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.solver import SudokuSolver
from src.validator import SudokuValidator
from puzzles.puzzle_collection import PuzzleCollection

class TestSudokuSolver(unittest.TestCase):
    
    def setUp(self):
        self.solver = SudokuSolver()
        self.debug_solver = SudokuSolver(debug=True)
    
    def test_easy_puzzle(self):
        """Test solving an easy puzzle."""
        solution = self.solver.solve(PuzzleCollection.EASY)
        self.assertIsNotNone(solution)
        self.assertTrue(SudokuValidator.is_valid_solution(solution))
    
    def test_medium_puzzle(self):
        """Test solving a medium puzzle."""
        solution = self.solver.solve(PuzzleCollection.MEDIUM)
        self.assertIsNotNone(solution)
        self.assertTrue(SudokuValidator.is_valid_solution(solution))
    
    def test_hard_puzzle(self):
        """Test solving a hard puzzle."""
        solution = self.solver.solve(PuzzleCollection.HARD)
        self.assertIsNotNone(solution)
        self.assertTrue(SudokuValidator.is_valid_solution(solution))
    
    def test_ai_escargot(self):
        """Test solving Inkala's AI Escargot."""
        print("\n🐌 Testing AI Escargot...")
        solution = self.debug_solver.solve(PuzzleCollection.AI_ESCARGOT)
        self.assertIsNotNone(solution)
        self.assertTrue(SudokuValidator.is_valid_solution(solution))
        
        stats = self.debug_solver.get_stats()
        print(f"AI Escargot Stats: {stats}")
    
    def test_platinum_blonde(self):
        """Test solving Inkala's Platinum Blonde."""
        print("\n💎 Testing Platinum Blonde...")
        solution = self.debug_solver.solve(PuzzleCollection.PLATINUM_BLONDE)
        self.assertIsNotNone(solution)
        self.assertTrue(SudokuValidator.is_valid_solution(solution))
        
        stats = self.debug_solver.get_stats()
        print(f"Platinum Blonde Stats: {stats}")
    
    def test_minimal_puzzle(self):
        """Test solving a minimal 17-clue puzzle."""
        solution = self.solver.solve(PuzzleCollection.MINIMAL_17)
        self.assertIsNotNone(solution)
        self.assertTrue(SudokuValidator.is_valid_solution(solution))
    
    def test_invalid_puzzle_format(self):
        """Test handling of malformed puzzle."""
        invalid_puzzles = [
            None,
            [],
            [[1, 2, 3]],  # Wrong size
            [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],  # Row too long
            [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']],  # Wrong type
        ]
        
        for invalid in invalid_puzzles:
            with self.assertRaises(ValueError):
                self.solver.solve(invalid)
    
    def test_invalid_puzzle_constraint(self):
        """Test handling of puzzle with constraint violations."""
        # Puzzle with duplicate in row
        invalid_constraint = [
            [1, 1, 0, 0, 0, 0, 0, 0, 0],  # Two 1's in first row
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        
        with self.assertRaises(ValueError):
            self.solver.solve(invalid_constraint)
    
    def test_empty_puzzle(self):
        """Test solving an empty puzzle (all zeros)."""
        empty = [[0] * 9 for _ in range(9)]
        solution = self.solver.solve(empty)
        self.assertIsNotNone(solution)
        self.assertTrue(SudokuValidator.is_valid_solution(solution))
    
    def test_already_solved_puzzle(self):
        """Test with an already solved puzzle."""
        solved = self.solver.solve(PuzzleCollection.EASY)
        solution = self.solver.solve(solved)
        self.assertIsNotNone(solution)
        self.assertEqual(solution, solved)

if __name__ == '__main__':
    unittest.main(verbosity=2)