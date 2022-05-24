import time
from RPi import GPIO
import threading

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository

from selenium import webdriver

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
temperatuurSensor = '/sys/bus/w1/devices/28-22cfd2000900/w1_slave'
# Code voor Hardware


def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)


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
    status = DataRepository.read_historiek()
    emit('B2F_historiek', {'historiek': status}, broadcast=True)
# Thread


def meetTemperatuur():
    global sensorFile
    while True:
        sensorFile = open(temperatuurSensor, 'r')
        for line in sensorFile:
            pos = line.find('t=')
            if pos > 0:
                temperatuur = int(line.strip(
                    '\n')[pos+2:])/1000.0
                print(f'Het is {temperatuur} °C')

        time.sleep(5)


def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=meetTemperatuur, args=(), daemon=True)
    thread.start()


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
        setup_gpio()
        start_thread()
        start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        sensorFile.close()
        GPIO.cleanup()
