import digitalio
import board

from bbq10keyboard import BBQ10Keyboard, STATE_PRESS, STATE_RELEASE, STATE_LONG_PRESS
from screen import Term
from buzzer import Buzzer


def singleton(cls):
    return cls()


@singleton
class Keyboard:
    KEY_SHIFT = 2
    KEY_UP = "\x01"
    KEY_LEFT = "\x03"
    KEY_DOWN = "\x02"
    KEY_RIGHT = "\x04"
    KEY_RETURN = "\n"
    KEY_DELETE = "\x08"
    KEY_ESC = "\x06"

    def __init__(self):
        i2c = board.I2C()
        while not i2c.try_lock():
            pass
        i2c.unlock()
        self.kbd = BBQ10Keyboard(i2c)

        self.line_history = []

    def is_esc(self):
        k = self.kbd.keys
        for key in k:
            if key[1] == self.KEY_ESC:
                return True
        return False

    def get_key(self):
        k = self.kbd.key
        if k:
            if k[0] == STATE_RELEASE:
                if k[1].isalpha():
                    return k[1].upper()
                else:
                    return k[1]
        else:
            return None

    def get_line(self):
        outline = ""
        # clear out any pending input
        t = self.kbd.keys
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

                elif self.__non_special(key):
                    Term.write(key)
                    outline += key
                else:
                    pass

    def get_char(self):
        while True:
            k = self.get_key()
            if k:
                return k

    def __non_special(self, key):
        if ord(key) > 32 and ord(key) < 126:
            return True
        else:
            return False
