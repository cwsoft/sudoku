"""
#######################################################################################
# Module for basic terminal color and cursor manipulations via a small and simple API.
# Under the hood ANSI escape sequences are printed to the terminals stdout.
#
# Some details about ANSI escape sequences can be found here:
# - https://de.wikipedia.org/wiki/ANSI-Escapesequenz
# - https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
#
# @module:    cterm
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
    """Basic terminal foreground color codes. For background colors simply increment by 10."""

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
    """Static class allowing basic cursor operations supported by most terminals."""

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
    """Static class to modify terminal colors and cursor position and output formated text."""

    class AutoReset(Enum):
        OFF = 0
        COLOR = 1
        CURSOR_POS = 2
        COLOR_AND_CURSOR_POS = 3

    @staticmethod
    def initialize(forecolor=Colors.RESET, backcolor=Colors.RESET):
        """Initialize terminal window (reset colors, clear output, set cursor to top-left position."""
        assert isinstance(forecolor, Colors), "Param 'forecolor' must be of Enum Colors."
        assert isinstance(backcolor, Colors), "Param 'backcolor' must be of Enum Colors."

        Terminal.set_color(forecolor, backcolor)
        Terminal.clear(mode=2)
        Cursor.set_pos(row=1, col=1)

    @staticmethod
    def clear(mode=2):
        """Clear terminal screen."""
        print(f"{Ansi.CSI.value}{mode}J")

    @staticmethod
    def set_color(forecolor=Colors.RESET, backcolor=Colors.RESET):
        """Set terminal fore- and background color to specified values. Colors must be of Enum Colors.
        Example: set_color(forecolor=Colors.RED, backcolor=Colors.YELLOW)."""
        assert isinstance(forecolor, Colors), "Param 'forecolor' must be of Enum Colors."
        assert isinstance(backcolor, Colors), "Param 'backcolor' must be of Enum Colors."
        print(f"{Ansi.CSI.value}{forecolor.value};{int(backcolor.value)+10}m", end="")

    @staticmethod
    def set_style(*styles):
        """Set terminal font styles to specified values. Font styles must be of Enum Styles.
        Example: set_style(Styles.BOLD, Styles.UNDERLINE)."""
        # Reset styles if no style was defined.
        if not styles:
            print(f"{Ansi.CSI.value}{Styles.RESET.value}m", end="")
            return

        # Loop through style enum args and apply all styles in sequence.
        for style in styles:
            assert isinstance(style, Styles), "Param(s) 'styles' must be of Enum Styles."
            print(f"{Ansi.CSI.value}{style.value}m", end="")

    @staticmethod
    def write(text, end="\n", row=None, col=None, forecolor=Colors.RESET, backcolor=Colors.RESET, auto_reset=AutoReset.OFF):
        """Write text to specified terminal position using specified fore- and background color. 
        Use Enum Terminal.AutoReset to reset colors and/or cursor position after writing to console."""
        assert isinstance(auto_reset, Terminal.AutoReset), "Param 'auto_reset' must be of Enum Terminal.AutoReset."
        if auto_reset in (Terminal.AutoReset.CURSOR_POS, Terminal.AutoReset.COLOR_AND_CURSOR_POS):
            Cursor.store_pos()

        # Set specified terminal cursor position.
        try:
            row, col = abs(int(row)), abs(int(col))
            Cursor.set_pos(row, col)
        except:
            pass

        # Set specified terminal colors.
        Terminal.set_color(forecolor, backcolor)

        # Write text to specified terminal position using defined colors.
        print(text, end=end)

        # Reset previous colors and cursor position depending on auto_reset value.
        if auto_reset in (Terminal.AutoReset.COLOR, Terminal.AutoReset.COLOR_AND_CURSOR_POS):
            Terminal.set_color(forecolor=Colors.RESET, backcolor=Colors.RESET)

        if auto_reset in (Terminal.AutoReset.CURSOR_POS, Terminal.AutoReset.COLOR_AND_CURSOR_POS):
            Cursor.restore_pos()
