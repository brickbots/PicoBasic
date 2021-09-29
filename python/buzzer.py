import time
import config

def singleton(cls):
    return cls()

@singleton
class Buzzer:

    def __init__(self):
        if config.HW != "cPython":
            import board
            import pwmio
            self.set_tone=self.__set_tone
            self.get_tone=self.__get_tone
            self.play=self.__play
            self.on = self.__on
            self.off = self.__off
            self.beep = self.__beep
        if config.HW == "picomputer":
            self.piezo = pwmio.PWMOut(board.GP0, variable_frequency=True)
        elif config.HW =="feather":
            self.piezo = pwmio.PWMOut(board.D13, variable_frequency=True)
        self.volume = 0.5
        self.duty_cycle = int(65535 * self.volume)
        self.set_tone(261)

    def set_volume(self, volume):
        self.volume = 0.5
        self.duty_cycle = int(65535 * self.volume)

    def get_volume(self):
        return self.volume

    def set_tone(self, freq):
        return

    def __set_tone(self, freq):
        self.piezo.frequency = freq

    def get_tone(self):
        return 0

    def __get_tone(self):
        return self.piezo.frequency

    def on(self):
        return

    def __on(self):
        self.piezo.duty_cycle = self.duty_cycle

    def off(self):
        return

    def __off(self):
        self.piezo.duty_cycle = 0

    def play(self, tone, duration):
        return

    def __play(self, tone, duration):
        self.set_tone(tone)
        self.on()
        time.sleep(duration)
        self.off()

    def beep(self):
        return

    def __beep(self):
        self.play(1600, .1)
