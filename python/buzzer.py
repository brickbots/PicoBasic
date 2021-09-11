import board
import time
import pwmio
import config

def singleton(cls):
    return cls()

@singleton
class Buzzer:
    def __init__(self):
        if config.HW == "picomputer":
            self.piezo = pwmio.PWMOut(board.GP0, variable_frequency=True)
        else:
            self.piezo = pwmio.PWMOut(board.D13, variable_frequency=True)
        self.volume = 0.5
        self.duty_cycle = int(65535 * self.volume)
        self.piezo.frequency = 261

    def set_volume(self, volume):
        self.volume = volume
        self.duty_cycle = int(65535 * self.volume)

    def get_volume(self):
        return self.volume

    def set_tone(self, freq):
        self.piezo.frequency = freq

    def get_tone(self):
        return self.piezo.frequency

    def on(self):
        self.piezo.duty_cycle = self.duty_cycle

    def off(self):
        self.piezo.duty_cycle = 0

    def play(self, tone, duration):
        self.set_tone(tone)
        self.on()
        time.sleep(duration)
        self.off()

    def beep(self):
        self.play(1600, .1)
