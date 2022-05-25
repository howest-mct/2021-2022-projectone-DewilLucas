import RPi.GPIO as GPIO
import time


class clKeypad:
    def __init__(self, parrij, parkolum) -> None:

        self.keypad = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            ["*", 0, "#"]
        ]

        self.rij = parrij
        self.kolum = parkolum
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        for j in range(len(self.kolum)):
            GPIO.setup(self.kolum[j], GPIO.OUT)
            GPIO.output(self.kolum[j], GPIO.LOW)
        for i in range(len(self.rij)):
            GPIO.setup(self.rij[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def vangToets(self):

        self.rowVal = -1
        for i in range(len(self.rij)):
            tmpRead = GPIO.input(self.rij[i])
            if tmpRead == 0:
                self.rowVal = i
        for j in range(len(self.kolum)):
            GPIO.setup(self.kolum[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if self.rowVal < 0 or self.rowVal > 3:
            self.exit()
            return
        GPIO.setup(self.rij[self.rowVal], GPIO.OUT)
        GPIO.output(self.rij[self.rowVal], GPIO.HIGH)

        self.colVal = -1
        for j in range(len(self.kolum)):
            tmpRead = GPIO.input(self.kolum[j])
            if tmpRead == 1:
                self.colVal = j
        if self.colVal < 0 or self.colVal > 2:
            self.exit()
            return
        self.exit()
        time.sleep(0.2)
        return self.keypad[self.rowVal][self.colVal]

    def exit(self):
        for i in range(len(self.rij)):
            GPIO.setup(self.rij[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.kolum)):
            GPIO.setup(self.kolum[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
