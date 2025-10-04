"""
Main script to demonstrate the Sudoku solver with various puzzles.
"""
from src.solver import SudokuSolver
from src.validator import SudokuValidator
from src.utils import GridFormatter
from puzzles.puzzle_collection import PuzzleCollection

def main():
    print("🧩 Advanced Sudoku Solver")
    print("=" * 50)
    
    solver = SudokuSolver(debug=True)
    puzzles = PuzzleCollection.get_all_puzzles()
    
    while True:
        print("\nAvailable puzzles:")
        valid_puzzles = {k: v for k, v in puzzles.items() if k != 'invalid'}
        
        for i, (name, _) in enumerate(valid_puzzles.items(), 1):
            clues = SudokuValidator.count_clues(puzzles[name])
            print(f"{i}. {name.replace('_', ' ').title()} ({clues} clues)")
        
        print("0. Exit")
        
        try:
            choice = input("\nSelect a puzzle (0-{}): ".format(len(valid_puzzles)))
            
            if choice == '0':
                print("Goodbye! 👋")
                break
            
            choice_idx = int(choice) - 1
            puzzle_name = list(valid_puzzles.keys())[choice_idx]
            puzzle = valid_puzzles[puzzle_name]
            
            print(f"\nSolving: {puzzle_name.replace('_', ' ').title()}")
            
            # Display original puzzle
            GridFormatter.print_grid(puzzle, "Original Puzzle")
            
            # Solve
            print("\n🔄 Solving...")
            solution = solver.solve(puzzle)
            
            if solution:
                # Display solution
                GridFormatter.print_grid(solution, "Solution")
                
                # Show statistics
                stats = solver.get_stats()
                print(f"\n📊 Statistics:")
                print(f"   Solve time: {stats['solve_time']:.4f} seconds")
                print(f"   Backtracks: {stats['backtrack_count']:,}")
                print(f"   Total attempts: {stats['attempts_count']:,}")
                print(f"   Constraint checks: {stats['constraint_checks']:,}")
                print(f"   Original clues: {SudokuValidator.count_clues(puzzle)}")
                
                # Verify solution
                if SudokuValidator.is_valid_solution(solution):
                    print("   ✅ Solution verified!")
                else:
                    print("   ❌ Solution validation failed!")
            else:
                print("❌ No solution found!")
                
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break

if __name__ == "__main__":
    main()