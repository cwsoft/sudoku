"""
#######################################################################################
# Script to solve Sudoko puzzles using a simple back tracking algorithm.
# Uses the module terminal to move the cursor and set colors in the Windows terminal.
#
# @module:    sudoku
# @platform:  Windows OS (tested with Windows 10 only)
# @requires:  csutils.cterm, pandas
# @author:    cwsoft
# @python:    3.8 or higher
#######################################################################################
"""
import argparse
import sys

import pandas as pd
from csutils.cterm import Colors, Styles, Cursor, Terminal


class Sudoku:
    def __init__(self, args):
        # Extract required and optional command line arguments.
        self.puzzlefile, self.space, self.interactive = args.puzzlefile, args.space, args.interactive

        # Read Sudoku puzzle file and draw initial board to terminal.
        self.read_puzzle_file(self.puzzlefile)
        self.print_board()

    def read_puzzle_file(self, puzzlefile):
        # Read Sudoku puzzle file and store board as 9x9 Numpy matrix.
        self.board_input = pd.read_csv(puzzlefile, sep=" ", comment="#", dtype="byte", header=None).to_numpy()
        assert self.board_input.shape == (9, 9)

        self.board, self.board_last_solution = self.board_input.copy(), None
        self.solutions_found, self.iteration_steps = 0, 0

    def print_board(self):
        """Print Sudoku input board as 9x9 matrix to terminal with input numbers highlighted green."""
        tpl_border = "|-+-+-+-|-+-+-+-|-+-+-+-|"
        tpl_values = "| {0} {0} {0} | {0} {0} {0} | {0} {0} {0} |"

        # Output puzzle file name and draw the initial empty board.
        print(f"Puzzle file: '{self.puzzlefile}'")
        for row in range(0, 9):
            if row % 3 == 0:
                print(tpl_border)
            print(tpl_values.format(self.space))
        print(tpl_border)

        # Fill input numbers from puzzle file into right board slots.
        self.set_board_numbers(inputs_only=True)

    def set_board_numbers(self, board=None, inputs_only=True):
        """Fill board with numbers from specified board. Input numbers are highlighted green."""
        board = self.board if board is None else board
        for row in range(9):
            for col in range(9):
                if self.board_input[row, col] > 0:
                    number = self.board_input[row, col]
                    self._set_board_number(number, row, col, forecolor=Colors.GREEN)
                else:
                    number = self.space if inputs_only else board[row, col]
                    self._set_board_number(number, row, col, forecolor=Colors.RESET)

    def solve_puzzle(self):
        """Solve Sudoku puzzle using backtracking algortithm."""
        # Disable cursor to avoid flickering when in interactive mode.
        if self.interactive:
            Cursor.disable()

        for row in range(9):
            for col in range(9):
                # Find first free slot in the board.
                if self.board[row][col] == 0:
                    # Find first number which can be placed in free board slot.
                    for number in range(1, 10):
                        if self._board_position_possible(number, row, col):
                            # Update free slot with actual number.
                            self.board[row, col] = number
                            if self.interactive:
                                self._set_board_number(number, row, col)

                            # Try to solve the board with the added number.
                            self.iteration_steps += 1
                            self.solve_puzzle()

                            # Reset last assigned number as no solution was found.
                            self.board[row, col] = 0
                            if self.interactive:
                                self._set_board_number(self.space, row, col)
                    return

        # Solver found a solution.
        if self.interactive:
            Cursor.enable()
        else:
            # Show all board numbers of the actual solution.
            self.set_board_numbers(inputs_only=False)

        # Store actual solution in case next run won´t find a new solution.
        # In this case we can print the last known solution in the main program.
        self.board_last_solution = self.board.copy()
        self.solutions_found += 1

        # Prompt user if we should check for another possible solution.
        print(f"Number of Iterations: {self.iteration_steps}" + " " * 15)
        if input("Check for another solution ([y]/n)? ").lower() == "n":
            print(f"\nSolver stopped on user request. Found {self.solutions_found} solution(s).")
            sys.exit()

        # Move cursor two lines up so next solution overwrites last two output lines instead of adding new lines.
        # Adding new lines would shift the board in the terminal and mess up with adding numbers to right spot.
        Cursor.up(pos=2)

        # Reset number of iterations for the next solution.
        self.iteration_steps = 0

    def _set_board_number(self, number, row, col, forecolor=None):
        """Transfer 9x9 row/col indices into terminal coordinates matching the initial empty board."""
        row_map = {0: 3, 1: 4, 2: 5, 3: 7, 4: 8, 5: 9, 6: 11, 7: 12, 8: 13}
        col_map = {0: 3, 1: 5, 2: 7, 3: 11, 4: 13, 5: 15, 6: 19, 7: 21, 8: 23}

        Terminal.write(number, row_map.get(row), col_map.get(col), forecolor, auto_reset=True)

    def _board_position_possible(self, number, row, col):
        """Check if number can be placed at given board[row][col] position."""

        # Check if given number already exists within the specified board row or column.
        if number in self.board[row, :] or number in self.board[:, col]:
            return False

        # Check if number already exists within 3x3 quadrant given by row/col index.
        row_idx, col_idx = (row // 3) * 3, (col // 3) * 3
        if number in self.board[row_idx : row_idx + 3, col_idx : col_idx + 3].flatten():
            return False

        # Number can be placed at board[row][col] slot.
        return True


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzlefile", help="File to the Sudoku puzzle to solve.", action="store")
    parser.add_argument("--space", help="Char used for free puzzle slots [Default: '.'].", action="store", default=".")
    parser.add_argument("--interactive", help="Outputs each single step (may slowdown hard problems).", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    # Parse command line arguments and quit program if required arguments are not specified.
    args = parse_args()

    # Initialize terminal.
    Terminal.initialize(forecolor=Colors.RESET, backcolor=Colors.RESET)

    try:
        # Initiate sudoko object and displays the puzzle specified via command line args.
        sudoku = Sudoku(args)

        # Prompt user to start the solver or to quit.
        if input("\nPress [Enter] to solve the puzzle or (q) to quit: ").lower() == "q":
            sys.exit()
        sudoku.solve_puzzle()

        # Print status message (move cursor down three rows to keep iteration number of last solution).
        Cursor.down(pos=3)
        if sudoku.solutions_found > 0 and not sudoku.board.all():
            print(f"No further solution found. There exists {sudoku.solutions_found} solution(s) for the input puzzle.")
            sudoku.set_board_numbers(board=sudoku.board_last_solution, inputs_only=False)
        else:
            print(f"Solver finished. Found {sudoku.solutions_found} solution(s) for the input puzzle.")

    except KeyboardInterrupt:
        pass

    finally:
        Cursor.enable()
        Terminal.set_style(Styles.RESET)
