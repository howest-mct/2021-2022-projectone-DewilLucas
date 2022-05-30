import time
from RPi import GPIO
import threading
import sys
from subprocess import check_output
import os
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository
from classes.mpuClass import MPU6050
from classes.keypadClass import clKeypad
from selenium import webdriver
from classes.TemperatuurClass import TemperatuurClass
from classes.lcdClass import Lcd
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# Variables
temperatuurSensor = '/sys/bus/w1/devices/28-22cfd2000900/w1_slave'
mpu = MPU6050(0x68)
rijKeypad = [9, 6, 22, 27]
kolumKeypad = [17, 16, 5]
button = 18
lcdPins = [23, 26, 19, 13]
E = 20
RS = 21
lcd = Lcd(E, RS, lcdPins)
# Code voor Hardware


def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button, GPIO.FALLING, pushed, 200)


def pushed(knop):
    time.sleep(5)
    print("TURNED OFF")
    os.system("sudo shutdown -h now")
    sys.exit()
    # quits the code


def schrijfLCD():

    lcd.init_LCD()  # kuis het eerst op
    ips = check_output(
        ['hostname', '--all-ip-addresses']).split()
    # Eerste ip die binnenkomt aka de ip van de ethernetpoort
    eth = ips[0]
    wlan = ips[1]  # de ip van de raspberry
    lcd.write_message(f"{eth.decode()}", 0x80)  # 0x80 is lijn 1 van de LCD
    lcd.write_message(f"{wlan.decode()}", 0xC0)  # 0xC0 is lijn 2 van de LCD


def leesMPU():
    while True:
        mpu.printAlles()
        # Checken voor open en dicht soon...


def leesTemperatuur():
    while True:
        lees = TemperatuurClass(temperatuurSensor)
        socketio.emit('B2F_temperatuur', {
            'temperatuur': lees.leesTemp()}, broadcast=True)


def meetTemperatuur():
    while True:
        huidigTemp = TemperatuurClass(temperatuurSensor)
        return huidigTemp.meetTemp()


def leesKeypad():
    while True:
        key = clKeypad(rijKeypad, kolumKeypad)
        toets = None
        if toets == None:
            toets = key.vangToets()
            if toets != None:
                print(toets)
                DataRepository.write_keypad(toets)
            else:
                pass


def leesHistoriek():
    pass


# Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)
# API ENDPOINTS


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!


# Thread


def start_thread():
    print("**** Starting THREAD ****")
    try:
        thread = threading.Thread(target=leesHistoriek, args=(), daemon=True)
        thread.start()
        temperatuur_thread()
        read_temperatuur_thread()
        MPU_thread()
        keypad_thread()
        lcd_thread()

    except Exception as ex:
        print(ex)


def lcd_thread():
    print("**** LCD DISPLAY ****")
    try:
        thread = threading.Thread(target=schrijfLCD, args=(), daemon=True)
        thread.start()
    except Exception as ex:
        print(ex)


def MPU_thread():
    print("**** MPU THREAD ****")
    try:
        thread = threading.Thread(target=leesMPU, args=(), daemon=True)
        thread.start()
    except Exception as ex:
        print(ex)


def temperatuur_thread():
    print("**** write Temperature THREAD ****")
    try:
        thread = threading.Thread(
            target=meetTemperatuur, args=(), daemon=True)
        thread.start()
    except Exception as ex:
        print(ex)


def keypad_thread():
    print("**** Read keypad THREAD *****")
    try:
        thread = threading.Thread(target=leesKeypad, args=(), daemon=True)
        thread.start()
    except Exception as ex:
        print(ex)


def read_temperatuur_thread():
    print("**** Read Temperature THREAD ****")
    try:
        thread = threading.Thread(target=leesTemperatuur, args=(), daemon=True)
        thread.start()
    except Exception as ex:
        print(ex)


def start_chrome_kiosk():
    import os

    os.environ['DISPLAY'] = ':0.0'
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--kiosk')
    # chrome_options.add_argument('--no-sandbox')
    # options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost")
    while True:
        pass


def start_chrome_thread():
    print("**** Starting CHROME ****")
    chromeThread = threading.Thread(
        target=start_chrome_kiosk, args=(), daemon=True)
    chromeThread.start()


# ANDERE FUNCTIES
if __name__ == '__main__':
    try:
        temp = TemperatuurClass(temperatuurSensor)
        setup_gpio()
        start_thread()
        start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        mpu.sluit()
        temp.sluitTemp()
        lcd.init_LCD()
        GPIO.cleanup()
