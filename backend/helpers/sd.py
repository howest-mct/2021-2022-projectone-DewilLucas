from RPi import GPIO
import time

databist = [13, 19, 26, 23, 24, 25, 12, 16]
tellerChar = 0
rs = 21
e = 20


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rs, GPIO.OUT)
    GPIO.setup(e, GPIO.OUT)
    for bit in databist:
        GPIO.setup(bit, GPIO.OUT, initial=GPIO.LOW)


def init_LCD():
    send_instruction(0b00111000)  # funtie set of 0x38
    send_instruction(0b00001111)  # Display on of 0xf
    send_instruction(0b00000001)  # clear display/cursor home of 0x01


def set_data_bits(value):
    mask = 0x80
    for i in range(8):
        GPIO.output(databist[i], value & (mask >> i))


def send_instruction(value):
    GPIO.output(rs, GPIO.LOW)
    GPIO.output(e, GPIO.HIGH)
    set_data_bits(value)
    GPIO.output(e, GPIO.LOW)
    time.sleep(0.01)


def send_charachter(value):
    GPIO.output(rs, GPIO.HIGH)
    GPIO.output(e, GPIO.HIGH)
    set_data_bits(value)
    GPIO.output(e, GPIO.LOW)
    time.sleep(0.2)


def write_message(message):
    global count
    count = 0
    for char in message:
        global tellerChar
        tellerChar += 1
        count += 1
        send_charachter(ord(char))
        if count == 16:
            send_instruction(0b10000000 | 0x40)
        if tellerChar == len(message):
            stopAlles()


def stopAlles():
    global count
    global tellerChar
    count = 0
    tellerChar = 0
    send_instruction(0b00000001)


try:
    setup()
    init_LCD()
    while True:
        write_message("ZADDDYYY")
        time.sleep(1)
except Exception as ex:
    print(ex)
finally:
    GPIO.cleanup()
    stopAlles()
    print("code Done")
