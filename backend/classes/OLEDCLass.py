import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os
# Use for I2C.
i2c = board.I2C()


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
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (self.oled.width, self.oled.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a white background
        draw.rectangle((0, 0, self.oled.width, self.oled.height),
                       outline=255, fill=255)
        self.font = ImageFont.load_default()

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.oled.width, self.oled.height),
                       outline=0, fill=0)
        # Pi Stats Display
        draw.text((0, 0), "Temperature: " +
                  temp, font=self.font, fill=255)
        draw.text((0, 16), aantal, font=self.font, fill=255)

        # Display image
        self.oled.image(image)
        self.oled.show()
        time.sleep(3)

    def tekenFoto(self):
        while True:
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_000_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_001_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_002_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_003_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_004_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_005_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_006_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_007_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_008_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_009_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_010_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_011_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_012_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_013_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_014_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_015_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_016_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_017_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_018_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_019_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_020_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_021_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_022_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_023_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_024_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_025_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_026_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_027_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_028_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_029_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            time.sleep(0.0001)
            image = Image.new("1", (self.oled.width, self.oled.height))
            image = Image.open(
                '/home/student/2021-2022-projectone-DewilLucas/nar/frame_030_delay-0.04s.jpg').convert('1')
            self.oled.image(image)
            self.oled.show()
            return 1
