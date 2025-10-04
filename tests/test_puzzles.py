"""
Test all puzzles in the collection for performance benchmarking.
"""
import unittest
import time
import sys
import os

# Fix import path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.solver import SudokuSolver
from src.validator import SudokuValidator
from puzzles.puzzle_collection import PuzzleCollection

class TestPuzzleCollection(unittest.TestCase):
    
    def setUp(self):
        self.solver = SudokuSolver(debug=False)
        self.puzzles = PuzzleCollection.get_all_puzzles()
    
    def test_all_valid_puzzles(self):
        """Test all valid puzzles and benchmark performance."""
        results = {}
        
        # Remove invalid puzzles from test
        valid_puzzles = {k: v for k, v in self.puzzles.items() 
                        if k not in ['invalid']}
        
        print(f"\nTesting {len(valid_puzzles)} puzzles...")
        print("-" * 70)
        
        for name, puzzle in valid_puzzles.items():
            print(f"Testing {name.upper().replace('_', ' ')} puzzle...", end=" ")
            
            start_time = time.time()
            try:
                solution = self.solver.solve(puzzle)
                solve_time = time.time() - start_time
                
                self.assertIsNotNone(solution, f"No solution found for {name}")
                self.assertTrue(SudokuValidator.is_valid_solution(solution), 
                              f"Invalid solution for {name}")
                
                stats = self.solver.get_stats()
                results[name] = {
                    'solve_time': solve_time,
                    'backtracks': stats['backtrack_count'],
                    'clues': SudokuValidator.count_clues(puzzle)
                }
                
                print(f"✅ {solve_time:.4f}s ({stats['backtrack_count']} backtracks)")
                
            except Exception as e:
                print(f"❌ FAILED: {e}")
                self.fail(f"Failed to solve {name}: {e}")
        
        # Print benchmark summary
        print("\n" + "="*70)
        print("BENCHMARK SUMMARY")
        print("="*70)
        print(f"{'Puzzle':<15} | {'Clues':<5} | {'Time (s)':<10} | {'Backtracks':<10}")
        print("-" * 70)
        
        total_time = 0
        for name, stats in sorted(results.items(), key=lambda x: x[1]['solve_time']):
            total_time += stats['solve_time']
            print(f"{name:<15} | {stats['clues']:>5} | {stats['solve_time']:>10.4f} | {stats['backtracks']:>10,}")
        
        print("-" * 70)
        print(f"{'TOTAL':<15} | {'':<5} | {total_time:>10.4f} | {'':<10}")

if __name__ == '__main__':
    unittest.main(verbosity=2)