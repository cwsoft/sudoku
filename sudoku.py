"""
#######################################################################################
# Script to solve Sudoko puzzles using a simple back tracking algorithm.
#
# @module:  sudoku
# @author:  cwsoft
# @python:  3.8 or higher
#######################################################################################
"""
import argparse
from datetime import datetime
import os
import sys

import pandas as pd


class Sudoku:
    def __init__(self, args):
        # Parse command line arguments, read sudoku input file and print initial board to console.
        self.sudokufile, self.space, self.interactive = args.sudokufile, args.space, args.interactive
        self.solutions = []
        self.read_board(self.sudokufile)

        # Print input board to console.
        self.print_board(desc="Sudoku input puzzle to solve")
        print()

        # Print initial starting board for the solver.
        if self.interactive:
            self.print_board(desc="Searching for possible solution(s)")
            print()

    def read_board(self, sudokufile):
        # Read Sudoku puzzle file and store board as 9x9 Numpy matrix.
        self.board = pd.read_csv(sudokufile, sep=" ", comment="#", dtype="byte", header=None).to_numpy()
        self.board_initial = self.board.copy()
        assert self.board.shape == (9, 9)

        # Initialize some variables for tracking solutions and time.
        self.nbr_iterations, self.nbr_solutions, self.start_time = 0, 0, datetime.now()

    def print_board(self, board=None, desc="", overwrite_last=False):
        """Prints puzzle as nine 3x3 quadrants on console."""
        board = self.board if board is None else board

        # Template for printing the 9x9 board.
        tpl_border = "|-+-+-+-|-+-+-+-|-+-+-+-|"
        tpl_values = "| {0} {1} {2} | {3} {4} {5} | {6} {7} {8} |"

        # Clear last printed sudoku puzzle if needed.
        if overwrite_last:
            # Used Escape sequences to move cursor 15 lines up to avoid flickering caused by os.system("clear").
            print("\033[A" * 15)

        print(desc, end="\n" if desc else "\r")
        for idx in range(0, 9):
            if idx % 3 == 0:
                # Surround each 3x3 quadrant with a border.
                print(tpl_border)

            # Replace all "0" values in actual board row with user defined space character.
            row_values = [number if number > 0 else self.space for number in board[idx, :]]
            print(tpl_values.format(*row_values))

        # Draw bottom board border.
        print(tpl_border)

    def solve_puzzle(self):
        """Iteratively solve Sudoku puzzle using backtracking."""
        for row in range(9):
            for col in range(9):
                # Find first free slot in the board.
                if self.board[row][col] == 0:
                    # Find first number which can be placed in free board slot.
                    for number in range(1, 10):
                        if self._board_position_possible(row, col, number):
                            # Update free slot with actual number and try to solve the updated board.
                            self.nbr_iterations += 1
                            self.board[row][col] = number
                            if self.interactive:
                                self.print_board(
                                    desc=f"Solution {self.nbr_solutions} [{self.nbr_iterations} steps]" + " " * 25,
                                    overwrite_last=True,
                                )
                            self.solve_puzzle()

                            # Reset last assigned number if no solution was found.
                            self.board[row][col] = 0
                    return

        # Store actual solution, increase counter and print actual solution.
        self.nbr_solutions += 1
        self.solutions.append(self.board.copy())

        ellapsed_time = round((datetime.now() - self.start_time).total_seconds(), 1)
        self.print_board(
            desc=f"Solution {self.nbr_solutions} [{ellapsed_time}s, {self.nbr_iterations} steps]",
            overwrite_last=self.interactive or (not self.interactive and self.nbr_solutions > 1),
        )

        # Ask user if we need to search for another solution.
        if input("Check if another solution exists [y/n]? ").lower() != "y":
            print("\nSudoku solver stopped on user request.")
            sys.exit()

        # Clear input prompt by moving cursor two lines up.
        print("\033[A" * 2)
        self.nbr_iterations, self.start_time = 0, datetime.now()

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
    parser.add_argument("sudokufile", help="Input file with Sudoku puzzle to solve.", action="store")
    parser.add_argument("--space", help="Char used for free puzzle slots [Default: '.'].", action="store", default=".")
    parser.add_argument("--interactive", help="Outputs each single step (may slowdown hard problems).", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    # Initiate sudoko object (reads puzzle file from args and outputs the puzzle to the console).
    args = parse_args()
    sudoku = Sudoku(args)

    try:
        # Try to find solutions for the given puzzle.
        sudoku.solve_puzzle()

        # If no further solution was found in interactive mode, we need to restore the last valid solution.
        if sudoku.interactive and sudoku.nbr_solutions > 0:
            sudoku.print_board(
                board=sudoku.solutions[-1],
                desc=f"Result of last valid Solution {sudoku.nbr_solutions}" + " " * 20,
                overwrite_last=True,
            )

        # Print status message
        print(f"\n\nNo more solution exists. Found {sudoku.nbr_solutions} solution(s).")

    except KeyboardInterrupt:
        pass
