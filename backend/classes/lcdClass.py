import RPi.GPIO as GPIO
import time

tellerChar = 0


class Lcd:
    def __init__(self, parE, parRS, lstdatabits) -> None:
        self.e = parE
        self.rs = parRS
        self.databits = lstdatabits
        self.setup()

    def setup(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.e, GPIO.OUT)
            GPIO.setup(self.rs, GPIO.OUT)
            for db in self.databits:
                GPIO.setup(db, GPIO.OUT, initial=GPIO.LOW)
            self.init_LCD()
        except Exception as ex:
            print(ex)

    def init_LCD(self):
        # false is omte zeggen dat we een command gaan vertsuren
        self.send_instruction(0x33, False)  # Initialize
        # zeg tegen display dat het in 4bits mode verstuurd word
        self.send_instruction(0x32, False)
        self.send_instruction(0x06, False)  # beweeg de cursor
        self.send_instruction(0x0C, False)  # zet de cursor uit
        self.send_instruction(0x28, False)  # 2 line display
        self.send_instruction(0x01, False)  # clear je display

    def send_instruction(self, bits, mode):
        # High bits
        # RS --> indien false: GPIO is low, klaar voor een instructie mee te geven
        GPIO.output(self.rs, mode)
        # RS --> indien True: GPIO is high, klaar om een karakter mee te geven
        for db in self.databits:
            GPIO.setup(db, GPIO.OUT, initial=GPIO.LOW)

        if bits & 0x10 == 0x10:
            # 00010000 eerste instructie voor eerste databit
            GPIO.output(self.databits[0], GPIO.HIGH)
        if bits & 0x20 == 0x20:
            # 00100000 tweede instructie voor tweede databit
            GPIO.output(self.databits[1], GPIO.HIGH)
        if bits & 0x40 == 0x40:
            # 01000000 derde instructie voor derde databit
            GPIO.output(self.databits[2], GPIO.HIGH)
        if bits & 0x80 == 0x80:
            # Je raad het nooit...10000000 vierde instructie voor vierde databit
            GPIO.output(self.databits[3], GPIO.HIGH)

        self.wacht()

        for db in self.databits:
            GPIO.setup(db, GPIO.OUT, initial=GPIO.LOW)
        if bits & 0x01 == 0x01:
            GPIO.output(self.databits[0], GPIO.HIGH)
        if bits & 0x02 == 0x02:
            GPIO.output(self.databits[1], GPIO.HIGH)
        if bits & 0x04 == 0x04:
            GPIO.output(self.databits[2], GPIO.HIGH)
        if bits & 0x08 == 0x08:
            GPIO.output(self.databits[3], GPIO.HIGH)
        self.wacht()

    def wacht(self):
        time.sleep(0.0001)
        GPIO.output(self.e, GPIO.HIGH)
        time.sleep(0.0001)
        GPIO.output(self.e, GPIO.LOW)
        # niet te lang wachten zodat het snel op het display komt en het klaar is voor volgende taak
        time.sleep(0.0001)

    def write_message(self, message, line):
        message = message.ljust(16, " ")
        self.send_instruction(line, False)
        for i in range(16):
            self.send_instruction(ord(message[i]), True)
