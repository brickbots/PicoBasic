from basic2040.interpreter import Interpreter
from picoterm import PicoTerm
from gc import mem_free


class PicoInterpreter(Interpreter):
    def main(self):

        banner = """
 .__ ._. __ .__..__ .__. __.._. __ 
 [__) | /  `|  |[__)[__](__  | /  `
 |   _|_\__.|__|[__)|  |.__)_|_\__.
        """
        self.__terminal.home()
        self.__terminal.print(banner)
        self.__terminal.print(str(mem_free()) + " Bytes Free")

        if not self.__terminal.is_esc():
            self.__terminal.buzzer.play(261, 0.2)
            self.__terminal.buzzer.play(361, 0.2)
            self.__terminal.buzzer.play(761, 0.6)
        else:
            # Load the regression test program
            self.program.load("BAS/TESTS.bas")
            self.__terminal.print("DEBUG MODE ON: Loaded TESTS")
            self.debug = True
        self.__interpreter()


PicoInterpreter(PicoTerm()).main()
