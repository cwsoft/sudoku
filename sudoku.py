"""
#######################################################################################
# Script to solve Sudoko puzzles using a simple back tracking algorithm.
#
# @module:    sudoku
# @platform:  Windows OS (tested with Windows 10 only)
# @author:    cwsoft
# @python:    3.8 or higher
#######################################################################################
"""
import argparse
import os
import sys

import pandas as pd


class Terminal:
    """Wrapper to manipulate Windows OS terminal cursor position and color using ANSI Escape sequences."""

    # You may need to adjust the terminals start position in case you are using a terminal other than Cmder.
    TERMINAL_TOP_LEFT_POS = (1, 1)

    # ANSI sequences to manipulate cursor position and foreground colors.
    SAVE_CURSOR_POS, RESTORE_CURSOR_POS = "\033[s", "\033[u"
    COLORS = {
        "default": "\033[0m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }

    def __init__(self):
        """Initialize the terminal."""
        self.clear()

    def move_up_down(self, pos):
        """Move cursor POS lines lines up or down."""
        if pos < 0:
            print(f"\033[{pos}A", end="")
        else:
            print(f"\033[{pos * -1}B", end="")

    def save_cursor_pos(self):
        """Save actual cursor position."""
        print(self.SAVE_CURSOR_POS, end="")

    def restore_cursor_pos(self):
        """Restore previously stored cursor position."""
        print(self.RESTORE_CURSOR_POS, end="")

    def clear(self):
        """Clear entire terminal output."""
        if os.name == "nt":
            os.system("cls")  # Windows OS
        else:
            os.system("clear")  # Linux/Unix like OS

    def tprint(self, row, col, msg="", color=None):
        """Outputs message in specified text color at defined terminal row/col position."""
        text_color = self.COLORS.get(color, self.COLORS["default"])
        x0, y0 = self.TERMINAL_TOP_LEFT_POS

        # Output message with specified color at given position.
        print(f"{text_color}\033[{x0 + row};{y0 + col}f{msg}{self.COLORS['default']}", end="")


class Sudoku:
    def __init__(self, args, terminal):
        # Extract command line arguments and store terminal object.
        self.puzzlefile, self.space, self.interactive = args.puzzlefile, args.space, args.interactive
        self.terminal = terminal

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

        # Fill in puzzle file numbers at respecitve board coordinates.
        self.set_board_numbers(inputs_only=True)

        # Prompt user to start solver or to quit.
        choice = input("\n\n\nPress [ENTER] to solve the puzzle or [Q] to quit: ").lower()
        if choice == "q":
            sys.exit()

        # Store actual terminal cursor position in memory.
        self.terminal.save_cursor_pos()

    def set_board_number(self, row_idx, col_idx, number, color=None):
        """Transfer 9x9 row/col indices into terminal coordinates matching initial board."""
        row_map = {0: 2, 1: 3, 2: 4, 3: 6, 4: 7, 5: 8, 6: 10, 7: 11, 8: 12}
        col_map = {0: 2, 1: 4, 2: 6, 3: 10, 4: 12, 5: 14, 6: 18, 7: 20, 8: 22}

        self.terminal.tprint(row_map.get(row_idx), col_map.get(col_idx), number, color)

    def set_board_numbers(self, board=None, inputs_only=True):
        """Fill board with numbers from specified board. Input numbers [1-9] are shown green."""
        board = self.board if board is None else board
        for row in range(9):
            for col in range(9):
                if self.board_input[row, col] > 0:
                    self.set_board_number(row, col, self.board_input[row, col], "green")
                else:
                    self.set_board_number(row, col, self.space if inputs_only else board[row, col], "default")

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
        # We store the actual solution in case next run won´t find a new solution.
        if not self.interactive:
            self.set_board_numbers(inputs_only=False)
        self.board_last_solution = self.board.copy()
        self.solutions_found += 1

        # Ask if we should check for another possible solution.
        # We restore actual cursor so input line does not move down with every new solution.
        self.terminal.restore_cursor_pos()
        print(f"Number of Iterations: {self.iteration_steps}")
        answer = input("Check for another solution [Y/N]? ").lower()
        if answer == "n":
            print(f"\nSolver stopped on user request. Found {self.solutions_found} solution(s).")
            sys.exit()

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
    terminal = Terminal()
    terminal.clear()

    # Initiate sudoko object.
    sudoku = Sudoku(args, terminal)

    try:
        # Try to find solutions for the given puzzle.
        sudoku.solve_puzzle()
        sudoku.terminal.restore_cursor_pos()

        # Print status message
        if sudoku.solutions_found > 0 and not sudoku.board.all():
            print(
                f"\n\n\nNo further solution found. There exists {sudoku.solutions_found} solution(s) for the input puzzle."
            )
            sudoku.terminal.save_cursor_pos()
            sudoku.set_board_numbers(board=sudoku.board_last_solution, inputs_only=False)
            sudoku.terminal.restore_cursor_pos()
        else:
            print(f"\n\n\nSolver finished. Found {sudoku.solutions_found} solution(s) for the input puzzle.")

    except KeyboardInterrupt:
        pass
