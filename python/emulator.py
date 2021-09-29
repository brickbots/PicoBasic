# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
This file implements a curses terminal class compatible with
Basic2040.  A terminal object needs to be provided to the
program class to enable BASIC print/input and other character
based IO operations.

The CursesTerm class uses curses to enable more sophisitcated
operation
"""

import curses
from picointerp import PicoInterpreter
from buzzer import Buzzer


class PicoEmulationTerm:
    buzzer = Buzzer

    def __init__(self, stdscr):

        # Turn off echo
        curses.noecho()

        # Don't wait for cr to process input
        curses.cbreak()

        # surpress visible cursor
        curses.curs_set(0)

        # Setup colors
        curses.init_color(10,100,200,800)
        curses.init_color(11,700,700,1000)
        curses.init_pair(2,11,10)
        curses.init_pair(1,10,11)

        # Setup outer window with room for border
        overscan_scr = stdscr.derwin(18, 54, 0, 0)
        overscan_scr.bkgd(curses.color_pair(1))

        # Draw border
        #overscan_scr.border(
        #    curses.ACS_CKBOARD,
        #    curses.ACS_CKBOARD,
        #    curses.ACS_CKBOARD,
        #    curses.ACS_CKBOARD,
        #    curses.ACS_CKBOARD,
        #    curses.ACS_CKBOARD,
        #    curses.ACS_CKBOARD,
        #    curses.ACS_CKBOARD,
        #)
        overscan_scr.refresh()

        # Now setup actual window to pass through
        self.__stdscr = overscan_scr.derwin(16, 52, 1, 1)
        self.__stdscr.bkgd(curses.color_pair(2))
        # accept arrows and other special chars
        self.__stdscr.keypad(True)
        self.__stdscr.scrollok(True)
        self.__line_history = []

    def print(self, to_print):
        """
        Print send the provided string to the terminal
        followed by a CR/LF
        """
        self.__stdscr.addstr(to_print + "\n", curses.color_pair(2))
        self.__stdscr.refresh()

    def write(self, to_write):
        """
        write sends the provided string to the terminal
        but does not include any other control chars
        """
        self.__stdscr.addstr(to_write, curses.color_pair(2))
        self.__stdscr.refresh()

    def enter(self):
        """
        Move down one line, and all the wya to the left.
        Equivilent of CR/LF combo
        """
        self.__stdscr.addstr("\n")
        self.__stdscr.refresh()

    def clear(self):
        """
        Clears the screen.
        Not Implemented here
        """
        self.__stdscr.clear()
        self.__stdscr.refresh()

    def home(self):
        """
        Returns the cursor to home position
        """
        self.__stdscr.move(0, 0)

    def cursor(self, x, y):
        """
        Moves the cursor to the specified x (column)
        and y (row) position on screen
        """
        # Substract one to map from BASIC 1 index to
        # Python 0 index
        self.__stdscr.move(y - 1, x - 1)

    def input(self):
        """
        Retrieves a string terminated by CR from the termnial
        This will echo to the screen
        """
        history_index = len(self.__line_history)
        curses.curs_set(1)
        self.__stdscr.refresh()

        retstr = ""
        key = self.__stdscr.getch()
        while key != 10:
            if key == curses.KEY_UP or key == curses.KEY_DOWN:
                if len(self.__line_history) > 0:

                    # backspace any current input
                    for i in range(len(retstr)):
                        self.backspace()

                    if key == curses.KEY_UP:
                        history_index -= 1
                        if history_index < 0:
                            curses.beep()
                            history_index = 0
                    else:
                        history_index += 1
                        if history_index > len(self.__line_history) - 1:
                            curses.beep()
                            history_index = len(self.__line_history) - 1
                    retstr = self.__line_history[history_index]
                    self.write(retstr)

            elif key == curses.KEY_LEFT:
                # backspace any current input
                for i in range(len(retstr)):
                    self.backspace()
                retstr = ""
            elif key == 127:
                # Backspace
                if len(retstr) > 0:
                    self.backspace()
                    retstr = retstr[:-1]
                else:
                    curses.beep()
            elif key < 32 or key > 126:
                pass
            else:

                retstr = retstr + chr(key)
                self.__stdscr.echochar(chr(key))
            key = self.__stdscr.getch()

        curses.curs_set(0)
        self.enter()
        self.__line_history.append(retstr)
        if len(self.__line_history) > 20:
            self.__line_history.pop(0)
        return retstr

    def backspace(self):
        """Handle a backspace"""
        self.__stdscr.echochar("\b")
        self.__stdscr.echochar(" ")
        self.__stdscr.echochar("\b")

    def get_char(self):
        """
        Retrieves a single character from the terminal
        and returns it ASCII code as integer.  This is
        to allow for various special codes/characters for
        buttons/arrows.

        Block until recieved, does not echo
        """
        return self.__stdscr.getch()

    def poll_char(self):
        """
        Checks keyboard state.  Returns zero if no key is pressed
        or integer representing the key (ASCII code for most keys).
        This allows special keys/buttons to be returned above or
        below normal ASCII code range

        Not implemnted here as it requires more OS specific
        business
        """
        return 0

        # This *should* work but does not seem to
        self.__stdscr.nodelay(True)
        pollchar = self.__stdscr.getch()
        self.__stdscr.nodelay(False)
        if pollchar == -1:
            pollchar = 0
        return pollchar

    def is_esc(self):
        if self.poll_char() == 27:
            return True
        else:
            return False


def main(stdscr):
    terminal = PicoEmulationTerm(stdscr)
    interp = PicoInterpreter(terminal)
    interp.main()


if __name__ == "__main__":
    curses.wrapper(main)
