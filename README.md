# 👀 Sudoku Solver - Python 3.8+
Simple Python Sudoku solver for Windows OS using backtracking algorithm and the great [Pandas package](https://pandas.pydata.org/docs/).

![Screenshot](./img/screenshot.png)

Note: The green numbers in the screenshot above are the input values loaded from the [puzzle file](./puzzles/easy.txt).

## Requirements
- Windows OS (tested with Windows 10)
- Windows Terminal supporting ANSI Escape Seuqences (cursor positioning and colors)

## Basic usage
Prepare a textfile with a Sudoku puzzle you can´t solve or you are too lazy to do manually. The Sudoko puzzle file consists of numbers [0-9] placed in a 9x9 grid, where the numer 0 indicates a free slot. Numers in columns are separated by single space char, rows are separated with a line break. Place # at the beginning of a line for adding comments ignored by the solver. Invoke the Sudoku solver with argument --interactive to see the backtracking algorithm in action.

```bash
usage: sudoku.py [-h] [--space SPACE] [--interactive] sudokufile

positional arguments:
  sudokufile     Input file with Sudoku puzzle to solve.

optional arguments:
  -h, --help     show this help message and exit
  --space SPACE  Char used for free puzzle slots [Default: '.'].
  --interactive  Outputs each single step (may slowdown hard problems).
```

Have fun 
cwsoft