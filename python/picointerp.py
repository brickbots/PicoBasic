from basic2040.interpreter import Interpreter
import config

if config.HW != 'cPython':
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
        if config.HW != 'cPython':
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


