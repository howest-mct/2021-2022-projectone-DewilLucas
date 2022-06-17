import RPi.GPIO as GPIO
import time
rijKeypad = [9, 6, 22, 27]
kolumKeypad = [17, 16, 5]
keypad = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

GPIO.setmode(GPIO.BCM)
for j in range(len(kolumKeypad)):
    GPIO.setup(kolumKeypad[j], GPIO.OUT)
    GPIO.output(kolumKeypad[j], GPIO.LOW)
for i in range(len(rijKeypad)):
    GPIO.setup(rijKeypad[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)


def vangToets():

    rowVal = -1
    for i in range(len(rijKeypad)):
        tmpRead = GPIO.input(rijKeypad[i])
        if tmpRead == 0:
            rowVal = i
    for j in range(len(kolumKeypad)):
        GPIO.setup(kolumKeypad[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    if rowVal < 0 or rowVal > 3:
        exit()
        return
    GPIO.setup(rijKeypad[rowVal], GPIO.OUT)
    GPIO.output(rijKeypad[rowVal], GPIO.HIGH)

    colVal = -1
    for j in range(len(kolumKeypad)):
        tmpRead = GPIO.input(kolumKeypad[j])
        if tmpRead == 1:
            colVal = j
    if colVal < 0 or colVal > 2:
        exit()
        return
    exit()
    time.sleep(0.2)
    return keypad[rowVal][colVal]


while True:
    vangToets()
