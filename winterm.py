"""
#######################################################################################
# ANSI sequence wrapper for windows terminals (WinTerm).
# Module to ease basic color and cursor manipulation for Windows terminals.
#
# For further infos see:
#  - https://de.wikipedia.org/wiki/ANSI-Escapesequenz
#  - https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
#
# @module:    winterm
# @platform:  Windows 10
# @author:    cwsoft
# @python:    3.8 or higher
#######################################################################################
"""

from enum import Enum


class Ansi(Enum):
    """Basic ANSI control sequences."""

    CSI = "\033["  # Control Sequence Intro
    OSC = "\033]"  # Operating System Command (not yet used)


class Colors(Enum):
    """Basic terminal foreground color codes."""

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39
    GREY = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97


class Styles(Enum):
    """Basic terminal styles supported by most terminals."""

    RESET = 0
    BOLD = 1
    UNDERLINE = 4
    REVERSE = 7


class Cursor:
    """Basic cursor operations supported by most terminals."""

    @staticmethod
    def disable():
        """Disable (hide) terminal cursor."""
        print(f"{Ansi.CSI.value}?25l", end="")

    @staticmethod
    def enable():
        """Enables (show) terminal cursor."""
        print(f"{Ansi.CSI.value}?25h", end="")

    @staticmethod
    def store_pos():
        """Store actual cursor position in memory."""
        print(f"{Ansi.CSI.value}s", end="")

    @staticmethod
    def restore_pos():
        """Restore cursor position from last stored position in memory."""
        print(f"{Ansi.CSI.value}u", end="")

    @staticmethod
    def set_pos(row=1, col=1):
        """Set cursor position to specified terminal row, col coordinates."""
        print(f"{Ansi.CSI.value}{row};{col}f", end="")

    @staticmethod
    def up(pos=1):
        """Move cursor up by pos rows."""
        print(f"{Ansi.CSI.value}{pos}A", end="")

    @staticmethod
    def down(pos=1):
        """Move cursor down by pos rows."""
        print(f"{Ansi.CSI.value}{pos}B", end="")

    @staticmethod
    def right(pos=1):
        """Move cursor to the right by pos cols (assuming LTR languages)."""
        print(f"{Ansi.CSI.value}{pos}C", end="")

    @staticmethod
    def left(pos=1):
        """Move cursor to the left by n-cols (assuming LTR languages)."""
        print(f"{Ansi.CSI.value}{pos}D", end="")


class Terminal:
    """Wrapper to manipulate Windows terminal using ANSI Escape sequences."""

    def __init__(self, forecolor=Colors.RESET, backcolor=Colors.RESET, auto_init=True):
        # Store terminal default forecolor and backcolor.
        assert isinstance(forecolor, Colors), "Param forecolor must be of Enum Colors!"
        assert isinstance(backcolor, Colors), "Param backcolor must be of Enum Colors!"
        self.default_forecolor, self.default_backcolor = forecolor, backcolor

        if auto_init:
            self.initialize()

    def initialize(self):
        """Initialize terminal window (reset colors, clear output, set cursor to top-left position."""
        self.set_color(self.default_forecolor, self.default_backcolor)
        self.clear(mode=2)
        Cursor.set_pos(row=1, col=1)

    def clear(self, mode=2):
        """Clear terminal screen."""
        print(f"{Ansi.CSI.value}{mode}J")

    def set_color(self, forecolor=Colors.RESET, backcolor=Colors.RESET):
        """Set terminal fore- and background color to specified values. Colors must be of Enum Colors.
        Example: set_color(forecolor=Colors.RED, backcolor=Colors.YELLOW)."""
        assert isinstance(forecolor, Colors), "Param forecolor must be of Enum Colors!"
        assert isinstance(backcolor, Colors), "Param backcolor must be of Enum Colors!"
        print(f"{Ansi.CSI.value}{forecolor.value};{int(backcolor.value)+10}m", end="")

    def set_style(self, *styles):
        """Set terminal font styles to specified values. Font styles must be of Enum Styles.
        Example: set_style(Styles.BOLD, Styles.UNDERLINE)."""
        # Reset styles if no or no valid style was defined.
        if not styles:
            print(f"{Ansi.CSI.value}{Styles.RESET.value}m", end="")
            return

        # Loop through style enum args and apply all styles in sequence.
        for style in styles:
            if isinstance(style, Styles):
                print(f"{Ansi.CSI.value}{style.value}m", end="")

    def write(self, text, end="\n", row=None, col=None, forecolor=Colors.RESET, backcolor=Colors.RESET, auto_reset=0):
        """Write text to specified terminal position using specified fore- and background color. 
        Set auto_reset {0: keep colors/pos, 1: reset color, keep pos, 2: resets color and pos}."""
        if auto_reset == 2:
            Cursor.store_pos()

        # Set specified terminal cursor position.
        try:
            row, col = abs(int(row)), abs(int(col))
            Cursor.set_pos(row, col)
        except:
            pass

        # Set specified terminal colors.
        self.set_color(forecolor, backcolor)

        # Write text to specified terminal position using defined colors.
        print(text, end=end)

        # Reset previous colors and cursor position depending on auto_reset value.
        if auto_reset > 0:
            self.set_color()
        if auto_reset == 2:
            Cursor.restore_pos()
