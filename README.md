# 👀 Sudoku Solver - Python 3.8+

Simple Sudoku solver using backtracking algorithm and the great [Pandas package](https://pandas.pydata.org/docs/).

## Basic usage
Prepare a textfile with a Sudoku puzzle you can´t solve or you are too lazy to do manually. The Sudoko puzzle file constists of numbers 0-9 in a 9x9 grid, where 0 indicates a free spot. Individual numbers are separated by a single space, rows are separeted by line break. You can use # at the line start for comment lines.

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