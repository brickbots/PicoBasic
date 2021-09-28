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


import config
from buzzer import Buzzer

if config.HW == 'picomputer':
    from picomputer_keyboard import Keyboard
else:
    from feather_keyboard import Keyboard
from screen import Term


class PicoTerm:
    def __init__(self):
        self.print = Term.print
        self.write = Term.write
        self.enter = Term.enter
        self.home = Term.home
        self.cursor = Term.cursor
        self.clear = Term.clear
        self.input = Keyboard.get_line
        self.get_char = Keyboard.get_char
        self.is_esc = Keyboard.is_esc
        self.buzzer = Buzzer

    def poll_char(self):
        """
        Checks keyboard state.  Returns zero if no key is pressed
        or integer representing the key (ASCII code for most keys).
        This allows special keys/buttons to be returned above or
        below normal ASCII code range

        Not implemnted here as it requires more OS specific
        business
        """
        k = Keyboard.get_char()
        if not k:
            return 0
        else:
            return ord(k)


