import RPi.GPIO as GPIO
import time
keypad = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

rij = [9, 6, 22, 27]
kolum = [17, 21, 5]
GPIO.setmode(GPIO.BCM)


def vangToets():

    for j in range(len(kolum)):
        GPIO.setup(kolum[j], GPIO.OUT)
        GPIO.output(kolum[j], GPIO.LOW)
    for i in range(len(rij)):
        GPIO.setup(rij[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    rowVal = -1
    for i in range(len(rij)):
        tmpRead = GPIO.input(rij[i])
        if tmpRead == 0:
            rowVal = i
    for j in range(len(kolum)):
        GPIO.setup(kolum[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    if rowVal < 0 or rowVal > 3:
        exit()
        return
    GPIO.setup(rij[rowVal], GPIO.OUT)
    GPIO.output(rij[rowVal], GPIO.HIGH)

    colVal = -1
    for j in range(len(kolum)):
        tmpRead = GPIO.input(kolum[j])
        if tmpRead == 1:
            colVal = j
    if colVal < 0 or colVal > 2:
        exit()
        return
    exit()
    return keypad[rowVal][colVal]


def exit():
    for i in range(len(rij)):
        GPIO.setup(rij[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for j in range(len(kolum)):
        GPIO.setup(kolum[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)


if __name__ == '__main__':
    while True:
        getal = None
        while getal == None:
            getal = vangToets()
        print(getal)
        time.sleep(0.3)
