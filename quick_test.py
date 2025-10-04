"""
Quick test script to verify the solver works correctly.
"""
from src.solver import SudokuSolver
from src.utils import GridFormatter
from puzzles.puzzle_collection import PuzzleCollection

def main():
    print("🚀 Quick Sudoku Solver Test")
    print("="*40)
    
    solver = SudokuSolver(debug=True)
    
    # Test with AI Escargot (the hardest puzzle)
    puzzle = PuzzleCollection.AI_ESCARGOT
    
    GridFormatter.print_grid(puzzle, "🐌 AI Escargot (Original)")
    
    print("\n🔄 Solving...")
    solution = solver.solve(puzzle)
    
    if solution:
        GridFormatter.print_grid(solution, "✅ Solution Found!")
        stats = solver.get_stats()
        print(f"\n📊 Performance Stats:")
        print(f"   ⏱️  Solve time: {stats['solve_time']:.4f} seconds")
        print(f"   🔄 Backtracks: {stats['backtrack_count']:,}")
        print(f"   🎯 Total attempts: {stats['attempts_count']:,}")
        print(f"   ✔️  Constraint checks: {stats['constraint_checks']:,}")
    else:
        print("❌ No solution found!")

if __name__ == "__main__":
    main()