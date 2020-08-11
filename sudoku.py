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
import sys

import pandas as pd


class Sudoku:
    def __init__(self, args):
        # Parse command line arguments, read sudoku input file and print initial board to console.
        self.sudokufile, self.space = args.sudokufile, args.space
        self.read_board(args.sudokufile)
        self.print_board(desc=f"Sudoku to solve")

        # Initialize some variables for tracking solutions and time.
        self.solutions_found, self.start_time = 0, datetime.now()

    def read_board(self, sudokufile):
        # Read Sudoku puzzle file and store board as 9x9 Numpy matrix.
        self.board = pd.read_csv(sudokufile, sep=" ", comment="#", dtype="byte", header=None).to_numpy()
        assert self.board.shape == (9, 9)

    def print_board(self, desc=""):
        """Prints puzzle as nine 3x3 quadrants on console."""
        # Template for printing the 9x9 board.
        tpl_border = "|-+-+-+-|-+-+-+-|-+-+-+-|"
        tpl_values = "| {0} {1} {2} | {3} {4} {5} | {6} {7} {8} |"

        print(desc, end="\n" if desc else "\r")
        for idx in range(0, 9):
            if idx % 3 == 0:
                # Surround each 3x3 quadrant with a border.
                print(tpl_border)

            # Replace all "0" values in actual board row with user defined space character.
            row_values = [number if number > 0 else self.space for number in self.board[idx, :]]
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
                        if self._check_slot(row, col, number):
                            # Update free slot with actual number and try to solve the updated board.
                            self.board[row][col] = number
                            self.solve_puzzle()
                            # Reset last assigned number if no solution was found.
                            self.board[row][col] = 0
                    return

        # Increase solution counter and print actual solution.
        self.solutions_found += 1
        ellapsed_time = round((datetime.now() - self.start_time).total_seconds(), 1)
        self.print_board(desc=f"\nSolution {self.solutions_found} [Time: {ellapsed_time}s]")

        # Ask user if we need to search for another solution.
        if input("Check if another solution exists [y/n]? ").lower() != "y":
            print("\nSudoku solver stopped on user request.")
            sys.exit()

        self.start_time = datetime.now()

    def _check_slot(self, row, col, number):
        """Check if number is allowed at board[row][col] slot an in the actual 3x3 quadrant."""

        # Check if given number already exists within the specified board row or column.
        if number in self.board[row, :] or number in self.board[:, col]:
            return False

        # Check if number already exists inside actual 3x3 quadrant.
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
    return parser.parse_args()


if __name__ == "__main__":
    # Initiate sudoko object (reads puzzle file from args and outputs the puzzle to the console).
    args = parse_args()
    sudoku = Sudoku(args)

    # Try to find solutions for the given puzzle.
    sudoku.solve_puzzle()

    # Print status message
    print(f"\nNo more solution exists. Found {sudoku.solutions_found} solution(s).")
