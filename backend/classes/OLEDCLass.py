# Created by: Michael Klements
# For Raspberry Pi Desktop Case with OLED Stats Display
# Base on Adafruit CircuitPython & SSD1306 Libraries
# Installation & Setup Instructions - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
# Use for I2C.
i2c = board.I2C()
batman = {
    0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x06, 0x00, 0x01, 0xc1, 0x83, 0x80, 0x07, 0xc3, 0xc3, 0xe0,
    0x0f, 0xe3, 0xc7, 0xf0, 0x0f, 0xff, 0xff, 0xf0, 0x1f, 0xff, 0xff, 0xf8, 0x1f, 0xff, 0xff, 0xf8,
    0x0f, 0xff, 0xff, 0xf0, 0x0f, 0x3b, 0xdc, 0xf0, 0x06, 0x01, 0x80, 0x60, 0x03, 0x01, 0x80, 0xc0,
    0x00, 0x00, 0x00, 0x00
}


class OLED:

    # Display Parameters
    def __init__(self, width, height, border) -> None:
        self.width = width
        self.height = height
        self.border = border
        self.oled_reset = digitalio.DigitalInOut(board.D4)
        self.oled = adafruit_ssd1306.SSD1306_I2C(
            self.width, self.height, i2c, addr=0x3C, reset=self.oled_reset)

    # Clear display.

    def Clear_oled(self):
        self.oled.fill(0)
        self.oled.show()

    def draw(self, temp, aantal):
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (self.oled.width, self.oled.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # image = Image.open('happycat_oled_64.ppm').convert('1')
        # Draw a white background
        draw.rectangle((0, 0, self.oled.width, self.oled.height),
                       outline=255, fill=255)
        self.font = ImageFont.load_default()

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.oled.width, self.oled.height),
                       outline=0, fill=0)
        # Pi Stats Display
        draw.text((0, 0), "temperatuur: " +
                  temp, font=self.font, fill=255)
        draw.text((0, 16), aantal, font=self.font, fill=255)

        # Display image
        self.oled.image(image)
        self.oled.show()
        time.sleep(.01)
