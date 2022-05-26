import time
from RPi import GPIO
GPIO.setmode(GPIO.BCM)

databist = [13, 19, 26, 23, 24, 25, 12, 16]
tellerChar = 0
rs = 21
e = 20


class clLCD:
    def __init__(self, rs, e, databist):
        self.e = e
        self.rs = rs
        GPIO.setup(rs, GPIO.OUT)
        GPIO.setup(e, GPIO.OUT)
        GPIO.setwarnings(False)
        self.databist = databist
        for bit in self.databist:
            GPIO.setup(bit, GPIO.OUT, initial=GPIO.LOW)

    def init_LCD(self):
        self.send_instrution(0b00111000)  # funtie set of 0x38
        self.send_instrution(0b00001111)  # Display on of 0xf
        self.send_instrution(0b00000001)  # clear display/cursor home of 0x01

    def send_instrution(self, value):
        GPIO.output(self.rs, GPIO.LOW)  # laag for instructie
        GPIO.output(self.e, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(self.e, GPIO.LOW)
        time.sleep(0.01)

    def set_data_bits(self, value):
        mask = 0x80
        for i in range(8):
            GPIO.output(self.databist[i], value & (mask >> i))

    def send_charachter(self, value):
        GPIO.output(self.rs, GPIO.HIGH)
        GPIO.output(self.e, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(self.e, GPIO.LOW)
        time.sleep(0.2)  # Zodat het leesbaar blijft bij het verplaatsen

    def write_message(self, bar, bericht):
        if bar != None:  # Als de bar niet niks is
            for i in range(int(bar)):
                # Waarde gevonden via https://theasciicode.com.ar/extended-ascii-code/block-graphic-character-ascii-code-219.html
                self.send_charachter(219)
        else:
            pass  # indien bar niks is=> negeer deze code
        count = 0  # Aantal karakters
        self.send_instrution(0b10000000 | 0x40)  # Start op 0
        for char in bericht[:16]:  # voor alle karakters in het bericht voor 16
            count += 1
            self.send_charachter(ord(char))
        # Voor alle karakters na 16 (buiten het lcd scherm)
        for char in bericht[16:]:
            count += 1
            self.send_instrution(0b00011000)  # verplaats je naar links
            self.send_charachter(ord(char))
        if count == len(bericht):
            self.send_instrution(0b00000001)  # Kuis het op

    def clearLCD(self):
        self.send_instrution(0b00000001)
        GPIO.cleanup()


if __name__ == "__main__":

    try:

        lcd = clLCD(rs, e, databist)  # class voor lcd
        lcd.init_LCD()  # initialiseer het lcd

        while True:
            bars = 5
            status = "123EZEZEZEZEZ\nERERRZREZRZERZRZR"
            lcd.write_message(bars, status)  # Schrijf op de LCD
            time.sleep(0.2)
    except KeyboardInterrupt:
        print('code gestopt')
    finally:
        lcd.clearLCD()  # Kuis alles op + Clear GPIO
        print("GPIO cleaned, code klaar")
