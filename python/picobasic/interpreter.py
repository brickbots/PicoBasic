#! /usr/bin/python

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

"""This class implements a BASIC interpreter that
presents a prompt to the user. The user may input
program statements, list them and run the program.
The program may also be saved to disk and loaded
again.

"""

from .basictoken import BASICToken as Token
from .lexer import Lexer
from .program import Program
from sys import stderr
from gc import mem_free

import config
if config.HW == 'picomputer':
    from picomputer_keyboard import Keyboard
else:
    from feather_keyboard import Keyboard
from buzzer import Buzzer
from screen import Term


def main():

    lexer = Lexer()
    program = Program()

    banner = """
 .__ ._. __ .__..__ .__. __.._. __ 
 [__) | /  `|  |[__)[__](__  | /  `
 |   _|_\__.|__|[__)|  |.__)_|_\__.
        """
    Term.home()
    Term.print(banner)
    Term.print(str(mem_free()) + " Bytes Free")
    if not Keyboard.is_esc():
        Buzzer.play(261, 0.2)
        Buzzer.play(361, 0.2)
        Buzzer.play(761, 0.6)
    else:
        # Load the regression test program
        program.load("TESTS")
        Term.print("DEBUG: Loaded REGRESSION")

    # Continuously accept user input and act on it until
    # the user enters 'EXIT'
    while True:

        Term.write("> ")
        stmt = Keyboard.get_line()

        try:
            tokenlist = lexer.tokenize(stmt)

            # Execute commands directly, otherwise
            # add program statements to the stored
            # BASIC program

            if len(tokenlist) > 0:

                # Exit the interpreter
                if tokenlist[0].category == Token.EXIT:
                    break

                # Add a new program statement, beginning
                # a line number
                elif tokenlist[0].category == Token.UNSIGNEDINT and len(tokenlist) > 1:
                    program.add_stmt(tokenlist)

                # Delete a statement from the program
                elif tokenlist[0].category == Token.UNSIGNEDINT and len(tokenlist) == 1:
                    program.delete_statement(int(tokenlist[0].lexeme))

                # Execute the program
                elif tokenlist[0].category == Token.RUN:
                    try:
                        program.execute()

                    except KeyboardInterrupt:
                        Term.print("Program terminated")

                # Report FREE memory
                elif tokenlist[0].category == Token.FREE:
                    Term.print(str(mem_free()) + " Bytes Free")

                # Clear the terminal
                elif tokenlist[0].category == Token.CLR:
                    Term.clear()
                    Term.home()

                # List the program
                elif tokenlist[0].category == Token.LIST:
                    program.list()

                # Save the program to disk
                elif tokenlist[0].category == Token.SAVE:
                    program.save(tokenlist[1].lexeme)
                    Term.print("Program written to file")

                # Load the program from disk
                elif tokenlist[0].category == Token.LOAD:
                    program.load(tokenlist[1].lexeme)
                    Term.print("Program read from file")

                # Delete the program from memory
                elif tokenlist[0].category == Token.NEW:
                    program.delete()

                # Unrecognised input
                else:
                    Term.print("Unrecognised input")
                    for token in tokenlist:
                        token.print_lexeme()
                        Term.enter()

        # Trap all exceptions so that interpreter
        # keeps running
        except Exception as e:
           Term.print(str(e))
           print(e)


if __name__ == "__main__":
    main()
