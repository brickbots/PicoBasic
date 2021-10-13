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
        page_top_index = 0
        if start_line:
            # Make sure first displayed page starts at the start_line
            for line_number in line_numbers:
                if int(line_number) >= start_line:
                    break
                    page_top = start_line
                else:
                    line_index += 1

            if line_index > len(line_numbers):
                # Hmmm.. never found the start line, start on the last page
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
                        out_line += " ".join(this_line) + "\n" + " " * indent
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
                self._terminal.write("Up/Dn - Lines / U/D - Pages / (S)top")
                opt_ = self._terminal.get_char()
                if opt_ == ord("S") or opt_ == ord("s"):
                    keep_listing = False
                elif opt_ == ord("U") or opt_ == ord("u"):
                    if page_top_index == 0:
                        self._terminal.beep()
                    else:
                        line_index = page_top_index - int(self._terminal.lines / 2) - 1
                        if line_index < 0:
                            line_index = 0
                        page_top_index = line_index
                        page_lines = 0
                elif opt_ == self._terminal.KEY_UP:
                    if page_top_index == 0:
                        self._terminal.beep()
                    else:
                        line_index = page_top_index - 1
                        page_top_index = line_index
                        page_lines = 0
                elif opt_ == self._terminal.KEY_DOWN:
                    line_index = page_top_index + 1
                    page_top_index = line_index
                    page_lines = 0
                else:
                    # Continue listing
                    self._terminal.clear()
                    self._terminal.home()

                    page_lines = 0
                    # Since we failed to print the last line we tried
                    # Back the index out one
                    line_index -= 1
                    page_top_index = line_index

            line_index += 1

            # Check for end of program
            if line_index > number_count - 1:
                keep_listing = False
