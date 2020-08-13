"""
#######################################################################################
# Script to solve Sudoko puzzles using a simple back tracking algorithm.
# Uses the module terminal to move the cursor and set colors in the Windows terminal.
#
# @module:    sudoku
# @platform:  Windows OS (tested with Windows 10 only)
# @author:    cwsoft
# @python:    3.8 or higher
#######################################################################################
"""
import argparse
import sys

import pandas as pd
from terminal import Terminal


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
        self.board, self.board_last_solution = self.board_input.copy(), None
        self.solutions_found, self.iteration_steps = 0, 0
        assert self.board.shape == (9, 9)

    def print_board(self):
        """Print Sudoku input board as 9x9 matrix to terminal with input numbers highlighted green."""
        tpl_border = "|-+-+-+-|-+-+-+-|-+-+-+-|"
        tpl_values = "| {0} {0} {0} | {0} {0} {0} | {0} {0} {0} |"

        # Print board description foloowed by the initial empty board grid.
        print(f"Puzzle file: '{self.puzzlefile}'")
        for row in range(0, 9):
            if row % 3 == 0:
                print(tpl_border)
            print(tpl_values.format(self.space))
        print(tpl_border)

        # Fill input numbers from puzzle file at respecitve board coordinates.
        self.set_board_numbers(inputs_only=True)

        # Prompt user to start solver or to quit.
        if input("\nPress [ENTER] to solve the puzzle or [Q] to quit: ").lower() == "q":
            sys.exit()

    def set_board_number(self, row_idx, col_idx, number, fg_color=None, bg_color=None, auto_reset=True):
        """Transfer 9x9 row/col indices into terminal coordinates matching initial board."""
        row_map = {0: 3, 1: 4, 2: 5, 3: 7, 4: 8, 5: 9, 6: 11, 7: 12, 8: 13}
        col_map = {0: 3, 1: 5, 2: 7, 3: 11, 4: 13, 5: 15, 6: 19, 7: 21, 8: 23}

        terminal.write(number, row_map.get(row_idx), col_map.get(col_idx), fg_color, bg_color, auto_reset)

    def set_board_numbers(self, board=None, inputs_only=True):
        """Fill board with numbers from specified board. Input numbers [1-9] are shown green."""
        terminal.exec(code="cursor_save")

        board = self.board if board is None else board
        for row in range(9):
            for col in range(9):
                if self.board_input[row, col] > 0:
                    self.set_board_number(row, col, self.board_input[row, col], fg_color="green", auto_reset=False)
                else:
                    self.set_board_number(row, col, self.space if inputs_only else board[row, col], auto_reset=False)

        # Reset previous cursor position and terminal colors.
        terminal.exec(code="cursor_load")
        terminal.exec(code="default")

    def solve_puzzle(self):
        """Solve Sudoku puzzle using backtracking algortithm."""
        for row in range(9):
            for col in range(9):
                # Find first free slot in the board.
                if self.board[row][col] == 0:
                    # Find first number which can be placed in free board slot.
                    for number in range(1, 10):
                        if self._board_position_possible(row, col, number):
                            # Update free slot with actual number and try to solve the updated board.
                            self.iteration_steps += 1
                            self.board[row, col] = number

                            if self.interactive:
                                self.set_board_number(row, col, number)
                            self.solve_puzzle()

                            # Reset last assigned number if no solution was found.
                            self.board[row, col] = 0
                            if self.interactive:
                                self.set_board_number(row, col, self.space)
                    return

        # Solver found a solution. Draw solved board if not in interactive mode.
        if not self.interactive:
            self.set_board_numbers(inputs_only=False)

        # Store actual solution in case next run won´t find a new solution.
        self.board_last_solution = self.board.copy()
        self.solutions_found += 1

        # Store cursor position so the number of iterations and the input line don´t move terminal cursor down with
        # every new solution as this would move the board out of place and skrew up the update of board numbers.
        terminal.exec(code="cursor_save")
        print(f"Number of Iterations: {self.iteration_steps}" + " " * 15)

        # Prompt user if we should check for another possible solution.
        if input("Check for another solution [Y/N]? ").lower() == "n":
            print(f"\nSolver stopped on user request. Found {self.solutions_found} solution(s).")
            sys.exit()

        # Reset cursor to previous position (next solution will overwrite the last two lines.)
        terminal.exec(code="cursor_load")

        # Reset number of iterations for the next solution.
        self.iteration_steps = 0

    def _board_position_possible(self, row, col, number):
        """Check if number can be placed at given board[row][col] posiiton."""

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

    # Create terminal object to use ANSI escape sequences for manipulation curosr position and text color.
    terminal = Terminal(terminal_fg_color="white", terminal_bg_color="black")
    terminal.exec("clear")

    try:
        # Initiate sudoko object and try to solve input puzzle specified via command line args.
        sudoku = Sudoku(args)
        sudoku.solve_puzzle()

        # Print status message. We add two lines to keep infos like number of iterations needed.
        print("\n" * 2)
        if sudoku.solutions_found > 0 and not sudoku.board.all():
            print(f"No further solution found. There exists {sudoku.solutions_found} solution(s) for the input puzzle.")
            terminal.exec(code="cursor_save")
            sudoku.set_board_numbers(board=sudoku.board_last_solution, inputs_only=False)
            terminal.exec(code="cursor_load")
        else:
            print(f"Solver finished. Found {sudoku.solutions_found} solution(s) for the input puzzle.")

    except KeyboardInterrupt:
        pass
