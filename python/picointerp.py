from basic2040.interpreter import Interpreter
import config

if config.HW != "cPython":
    from gc import mem_free


class PicoInterpreter(Interpreter):
    def main(self):

        banner = """
 .__ ._. __ .__..__ .__. __.._. __
 [__) | /  `|  |[__)[__](__  | /  `
 |   _|_\__.|__|[__)|  |.__)_|_\__.
        """
        self._terminal.home()
        self._terminal.print(banner)
        if config.HW != "cPython":
            self._terminal.print(str(mem_free()) + " Bytes Free")
        else:
            self._terminal.print("102400 Bytes Free")

        if not self._terminal.is_esc():
            self._terminal.buzzer.play(261, 0.2)
            self._terminal.buzzer.play(361, 0.2)
            self._terminal.buzzer.play(761, 0.6)
        else:
            # Load the regression test program
            self.program.load("BAS/TESTS.bas")
            self._terminal.print("DEBUG MODE ON: Loaded TESTS")
            self.debug = True
        self._interpreter()

    def _list(self, start_line=None, end_line=None):
        """
        Handles textual listing of a program to the screen.
        can be overwritten to implement pagination or other
        hardware or use case specific behavior
        """
        line_numbers = self.program.line_numbers()
        if len(line_numbers) == 0:
            return

        line_index = 0
        if start_line:
            # Make sure first displayed page starts at the start_line
            for line_number in line_numbers:
                if int(line_number) >= start_line:
                    break
                else:
                    line_index += 1

            if line_index > len(line_numbers):
                # Hmmm.. never found the start line
                line_index = line_index - int(self._terminal.lines * 0.75)
                if line_index < 0:
                    line_index = 0

        # Okay, we know where to start, now get to it!
        keep_listing = True
        number_count = len(line_numbers)
        page_lines = 0
        while keep_listing:
            out_line = ""
            # split line as needed
            prog_line = self.program.str_statement(line_numbers[line_index])
            if len(prog_line) > self._terminal.cols:
                line_split = prog_line.split(" ")
                col_count = 0
                this_line = []
                indent = len(line_split[0]) + 1
                for token in line_split:
                    if col_count + len(token) >= self._terminal.cols:
                        out_line += (
                            " ".join(this_line) + "\n" + " " * indent
                        )
                        page_lines += 1
                        this_line = [token]
                        col_count = indent
                    else:
                        this_line.append(token)
                        # Add this token's length + the space that follows
                        col_count += len(token) + 1
                out_line += " ".join(this_line) + "\n"
                page_lines += 1
            else:
                out_line = prog_line + "\n"
                page_lines += 1

            if page_lines <= self._terminal.lines - 1:
                self._terminal.write(out_line)
            else:
                self._terminal.cursor(1, self._terminal.lines)
                self._terminal.write("PAGE")
                self._terminal.get_char()
                page_lines = 0
                # Since we failed to print the last line we tried
                # Back the index out one
                line_index -= 1

            line_index += 1
            if line_index > number_count - 1:
                keep_listing = False
