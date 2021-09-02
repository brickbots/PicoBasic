import digitalio
import board
from screen import Term
from buzzer import Buzzer


def singleton(cls):
    return cls()


@singleton
class Keyboard:
    KEY_SHIFT = 2
    KEY_UP = 3
    KEY_LEFT = 4
    KEY_DOWN = 5
    KEY_RIGHT = 6
    KEY_RETURN = "\n"
    KEY_DELETE = 8
    KEY_ESC = 9

    direct_keys = [
        [" ", ",", "M", "N", "B", KEY_DOWN],
        [KEY_RETURN, "L", "K", "J", "H", KEY_LEFT],
        ["P", "O", "I", "U", "Y", KEY_UP],
        [KEY_SHIFT, "Z", "X", "C", "V", KEY_RIGHT],
        ["A", "S", "D", "F", "G", "=", KEY_DOWN],
        ["Q", "W", "E", "R", "T", KEY_DELETE],
    ]

    symbol_keys = [
        [" ", ".", ":", ";", '"', KEY_DOWN],
        [KEY_RETURN, "-", "*", "&", "+", KEY_LEFT],
        ["0", "9", "8", "7", "6", KEY_UP],
        [KEY_SHIFT, "(", ")", "?", "/", KEY_RIGHT],
        ["!", "@", "#", "$", "%", "=", KEY_DOWN],
        ["1", "2", "3", "4", "5", KEY_DELETE],
    ]

    col_pins = [
        digitalio.DigitalInOut(board.GP1),
        digitalio.DigitalInOut(board.GP2),
        digitalio.DigitalInOut(board.GP3),
        digitalio.DigitalInOut(board.GP4),
        digitalio.DigitalInOut(board.GP5),
        digitalio.DigitalInOut(board.GP14),
    ]
    row_pins = [
        digitalio.DigitalInOut(board.GP6),
        digitalio.DigitalInOut(board.GP9),
        digitalio.DigitalInOut(board.GP15),
        digitalio.DigitalInOut(board.GP8),
        digitalio.DigitalInOut(board.GP7),
        digitalio.DigitalInOut(board.GP22),
    ]

    line_history = []

    def __init__(self):
        # Setup shift lock indicator
        self.led = digitalio.DigitalInOut(board.GP25)
        self.led.direction = digitalio.Direction.OUTPUT
        self.led.value = False

        for pin in self.col_pins:
            pin.direction = digitalio.Direction.OUTPUT
            pin.value = True

        for pin in self.row_pins:
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP

        self.out_key = None
        self.last_key = None
        self.current_key = None

    def is_esc(self):
        self.col_pins[5].value = False
        if self.row_pins[4].value == False:
            self.col_pins[5].value = True
            return True
        else:
            self.col_pins[5].value = True
            return False

    def scan_kb(self):
        scan_key = None
        debounce_key = None
        for col_index in range(6):
            self.col_pins[col_index].value = False
            for row_index in range(6):
                if self.row_pins[row_index].value == False:
                    if self.led.value:
                        # shifted...
                        scan_key = self.symbol_keys[row_index][col_index]
                    else:
                        scan_key = self.direct_keys[row_index][col_index]

            self.col_pins[col_index].value = True

        if scan_key == self.last_key:
            debounce_key = scan_key
        self.last_key = scan_key

        if self.current_key != debounce_key:
            self.current_key = debounce_key

            if self.led.value and debounce_key in [
                self.KEY_SHIFT,
                " ",
                self.KEY_ESC,
                self.KEY_RETURN,
            ]:
                self.led.value = False
            else:
                if debounce_key == self.KEY_SHIFT:
                    self.led.value = True
            if debounce_key != self.KEY_SHIFT:
                self.out_key = debounce_key
        else:
            self.out_key = None

        self.last_key = scan_key
        # print(scan_key, debounce_key, self.last_key, self.current_key, self.out_key)

    def get_key(self):
        self.scan_kb()
        return self.out_key

    def get_line(self):
        outline = ""
        history_index = len(self.line_history)
        while True:
            key = self.get_key()
            if key:
                if key == self.KEY_DELETE:
                    if len(outline) > 0:
                        Term.backspace()
                        outline = outline[:-1]
                    else:
                        Buzzer.beep()
                elif key == "\n":
                    Term.enter()
                    self.line_history.append(outline)
                    if len(self.line_history) > 20:
                        self.line_history.pop(0)
                    return outline

                elif key == self.KEY_UP or key == self.KEY_DOWN:
                    # backspace any current input
                    for i in range(len(outline)):
                        Term.backspace()

                    if key == self.KEY_UP:
                        history_index -= 1
                        if history_index < 0:
                            Buzzer.beep()
                            history_index = 0
                    else:
                        history_index += 1
                        if history_index > len(self.line_history) - 1:
                            Buzzer.beep()
                            history_index = len(self.line_history) - 1
                    outline = self.line_history[history_index]
                    Term.write(outline)

                elif key == self.KEY_LEFT:
                    # backspace any current input
                    for i in range(len(outline)):
                        Term.backspace()
                    outline = ""

                elif type(key) == int:
                    pass
                else:
                    Term.write(key)
                    outline += key

    def get_char(self):
        self.scan_kb()
        while self.out_key == None:
            self.scan_kb()

        return self.out_key
