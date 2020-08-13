"""
#######################################################################################
# Wrapper to manipulate Windows OS terminal cursor position and color by using
# ANSI Escape sequences. 
#
# @module:    terminal
# @platform:  Windows OS (tested with Windows 10 only)
# @author:    cwsoft
# @python:    3.8 or higher
#######################################################################################
"""


class Terminal:
    """Wrapper to manipulate Windows OS terminal cursor position and color using ANSI Escape sequences."""

    # ANSI sequences to manipulate cursor position and foreground colors.
    CODES = {
        # General commands
        "clear": "\033[2J",
        "default": "\033[0m",
        # Cursor positioning
        "cursor_hide": "\033[?25l",
        "cursor_show": "\033[?25h",
        "cursor_save": "\033[s",
        "cursor_load": "\033[u",
        "cursor_up": "\033[{pos}A",
        "cursor_down": "\033[{pos}A",
        "cursor_set": "\033[{row};{col}f",
        # Terminal fore- and background colors {pos: 3:=foreground, 4:=background}
        # Note: pos is automatically set in method self.color().
        "black": "\033[{pos}0m",
        "red": "\033[{pos}1m",
        "green": "\033[{pos}2m",
        "yellow": "\033[{pos}3m",
        "blue": "\033[{pos}4m",
        "magenta": "\033[{pos}5m",
        "cyan": "\033[{pos}6m",
        "white": "\033[{pos}7m",
    }

    def __init__(self, terminal_fg_color="white", terminal_bg_color="black", auto_init=False):
        """Initiates the terminal class with a default terminal fore- and background color.
        Change this settings in case you changed the default Windows terminal colors."""
        self.terminal_fg_color, self.terminal_bg_color = terminal_fg_color, terminal_bg_color

        if auto_init:
            self.initialize()

    def initialize(self):
        """Initializes the terminal. Clear output and set cursor to defined start position."""
        self.exec(code="clear")
        self.set_pos(row=1, col=1)

    def exec(self, code, **kwargs):
        """Executes given ANSI code sequence and replaces any optional placeholder(s) with values defined as kwargs."""
        assert code in self.CODES
        print(self.CODES.get(code).format(**kwargs), end="")

    def set_color(self, fg_color, bg_color=None):
        """Set terminal fore- and background colors to given values.
        Note: {pos} is a placeholder defined in ANSI colors (3:=Foreground, 4:=Background)."""
        self.exec(code=fg_color if fg_color in self.CODES else self.terminal_fg_color, pos="3")
        self.exec(code=bg_color if bg_color in self.CODES else self.terminal_bg_color, pos="4")

    def set_pos(self, row, col):
        """Set terminal cursor position to given row and col values."""
        if not row is None and not col is None:
            self.exec(code="cursor_set", row=row, col=col)

    def write(self, text, row=None, col=None, fg_color=None, bg_color=None, auto_reset=True):
        """Write text to specified terminal position using defined colors. Cursor position and 
        terminal colors are reset to previous values/defaults after output by default."""
        if auto_reset:
            self.exec(code="cursor_save")

        # Set cursor position and terminal colors.
        self.set_pos(row, col)
        self.set_color(fg_color, bg_color)

        # Write text to console and reset colors afterwards.
        print(text, end="")

        # Reset previous cursor position and terminal colors if needed.
        if auto_reset:
            self.exec(code="cursor_load")
            self.exec(code="default")
