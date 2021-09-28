import displayio
import terminalio
import busio
import board
import config

displayio.release_displays()
if config.HW == "feather":
    # If using a feather, assume keybord_feather
    from adafruit_ili9341 import ILI9341

    spi = board.SPI()
    while not spi.try_lock():
        pass
    spi.configure(baudrate=62500000)  # This is the theoretical max for RP2040
    spi.unlock()
    tft_cs = board.D9
    tft_dc = board.D10

    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
    display = ILI9341(display_bus, width=320, height=240)

else:
    # Assume PICOmputer
    from rsu_st7789 import ST7789

    spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)

    while not spi.try_lock():
        pass
    spi.configure(baudrate=62500000)  # This is the theoretical max for RP2040
    spi.unlock()
    tft_cs = board.GP17
    tft_dc = board.GP16

    display_bus = displayio.FourWire(
        spi, command=tft_dc, chip_select=tft_cs, reset=board.GP21
    )

    display = ST7789(
        display_bus,
        width=240,
        height=240,
        rowstart=00,
        colstart=80,
        backlight_pin=board.GP20,
    )


def singleton(cls):
    return cls()


@singleton
class Term:
    display = display
    # top_group = displayio.Group(max_size=3, scale=1)
    top_group = displayio.Group(scale=1)

    # Create a bitmap with one colors
    bg_bitmap = displayio.Bitmap(display.width, display.height, 1)

    # Create a two color palette
    bg_palette = displayio.Palette(1)
    bg_palette[0] = 0x9999FF

    # Create a TileGrid using the Bitmap and Palette
    bg_tile_grid = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)

    # Add the TileGrid to the Group
    top_group.append(bg_tile_grid)
    display.show(top_group)

    bb = terminalio.FONT.get_bounding_box()
    font_height = bb[1]
    font_width = bb[0]
    lines = int(display.height / font_height) - 1
    cols = int(display.width / font_width) - 1

    def __init__(self):
        self.pal = displayio.Palette(2)
        self.pal[1] = 0x9999FF
        self.pal[0] = 0x000088

        # default width/height: 6/14
        # bitocra-13: 7/15

        self.tg = displayio.TileGrid(
            terminalio.FONT.bitmap,
            pixel_shader=self.pal,
            width=self.cols,
            height=self.lines,
            tile_width=self.font_width,
            tile_height=self.font_height,
            x=int((self.display.width - (self.cols * self.font_width))/2),
            y=int((self.display.height - (self.lines * self.font_height))/2),
        )
        self.terminal = terminalio.Terminal(self.tg, terminalio.FONT)

        self.top_group.append(self.tg)

        self.__blank_line = ""
        for i in range(self.cols - 1):
            self.__blank_line += " "

    def write(self, string):
        self.terminal.write(bytes(str(string), "ascii"))

    def escape(self, code):
        self.write(chr(27) + "" + code)

    def enter(self):
        self.write("\n\r")

    def backspace(self):
        self.write("\b")
        self.write(" ")
        self.write("\b")

    def clear_line(self):
        self.write("\r")
        self.write(self.__blank_line)
        self.write("\r")

    def print(self, string):
        self.write(string.replace("\n", "\n\r"))
        self.enter()

    def clear(self):
        self.escape("[2J")

    def home(self):
        self.escape("[;H")

    def cursor(self, x, y):
        if x > self.cols:
            x = self.cols
        if y > self.lines:
            y = self.lines
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        self.escape("[" + str(y) + ";" + str(x) + "H")
