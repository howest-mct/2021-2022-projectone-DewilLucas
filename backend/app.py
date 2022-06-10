import time
from RPi import GPIO
import threading
import sys
from subprocess import check_output
import os
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from repositories.DataRepository import DataRepository
from classes.mpuClass import MPU6050
from classes.keypadClass import clKeypad
from selenium import webdriver
from classes.TemperatuurClass import TemperatuurClass
from classes.lcdClass import Lcd
from classes.OLEDCLass import OLED
import random
from datetime import datetime
from datetime import date

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
oled = OLED(128, 64, 5)
lees = TemperatuurClass(temperatuurSensor)
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


def geefAantal():
    while True:
        totaalAanwezig = DataRepository.aantal_aanwezigeproducten()
        if totaalAanwezig == -1:
            print(totaalAanwezig)
            return "Geen aanwezige producten"
        else:
            print(totaalAanwezig)
            return f"Aantal producten:{totaalAanwezig['totaalAanwezig']}"


def showOled():
    while True:
        huidigeTemp = leesTemperatuur()
        print(huidigeTemp)
        aanwezig = geefAantal()
        print(aanwezig)
        uitvoerTemp = f"{str(huidigeTemp['waarde'])}°C"
        uitvoerAantal = aanwezig
        oled.Clear_oled()
        oled.draw(uitvoerTemp, uitvoerAantal)
        time.sleep(10)
        oled.Clear_oled()
        pic = oled.tekenFoto()
        if(pic == 1):
            oled.Clear_oled()
            oled.draw(uitvoerTemp, uitvoerAantal)


def converteerListNaarStr(lstString):
    verwijder1haak = lstString.replace("[", "")
    verwijder2haak = verwijder1haak.replace("]", "")
    verwijderkomma = verwijder2haak.replace(",", "")
    getallen = verwijderkomma.replace(" ", "")
    return getallen


def barcodeInput(invoer=""):
    barcode = invoer
    if barcode == "":
        pass
    else:
        print(barcode)
        lcd.init_LCD()
        print("**** Read keypad THREAD *****")
        try:
            DataRepository.write_scan_history(barcode)
            zoek = DataRepository.zoekByBaarcode(barcode)
            if zoek == -1:
                DataRepository.write_barcode(barcode)
                lcd.write_message("Verander de naam", 0X80)
                lcd.write_message("Op de webapp", 0xC0)
                print("nieuwe product ingevoegd")
                time.sleep(2)
                lcd.init_LCD()
                zoek = DataRepository.zoekByBaarcode(barcode)

            lcd.write_message("Geef vervaldatum", 0x80)
            lstDatum = []
            thread = threading.Thread(
                target=leesKeypad, args=(), daemon=True)
            thread.start()

            while len(lstDatum) != 8:
                waarde = leesKeypad()
                if waarde == None or waarde == "#" or waarde == "*":
                    pass
                else:
                    lstDatum.append(waarde)
                    strDatum = str(lstDatum)
                    newStrdatum = converteerListNaarStr(strDatum)
                    finalString = f"{newStrdatum[:2]}-{newStrdatum[2:4]}-{newStrdatum[4:len(newStrdatum)]}"
                    lcd.write_message(finalString, 0XC0)
            else:

                eersteGetal = str(lstDatum[0]) + str(lstDatum[1])
                tweedeGetal = str(lstDatum[2]) + str(lstDatum[3])
                jaartal = str(lstDatum[4])+str(lstDatum[5]) + \
                    str(lstDatum[6]) + str(lstDatum[7])
                datumke = f"{jaartal}-{tweedeGetal}-{eersteGetal}"
                try:
                    d = datetime.strptime(datumke, '%Y-%m-%d').date()
                    # d = datetime.datetime.date(int(jaartal), int(
                    #    tweedeGetal), int(eersteGetal))
                    huidigeDatum = date.today()
                    verschil = d-huidigeDatum
                    lcd.init_LCD()
                    lcd.write_message("Hoeveel?", 0x80)
                    lstAantal = []

                    aantal = ""
                    while aantal != "#":

                        aantal = leesKeypad()
                        if aantal == None or aantal == "#" or aantal == "*":
                            pass
                        else:
                            lstAantal.append(aantal)
                            strAantal = str(lstAantal)
                            convStrAantal = converteerListNaarStr(
                                strAantal)
                            global final
                            final = f"{convStrAantal}"
                            lcd.write_message(final, 0XC0)

                    DataRepository.add_product_in_inventory(
                        zoek['idproduct'], d, verschil.days, int(final))
                    print(d)
                    lcd.init_LCD()
                    lcd.write_message("Dit is een...", 0x80)
                    lcd.write_message("Succes! :)", 0XC0)
                    time.sleep(3)
                    schrijfLCD()
                except Exception as ex:
                    print("datum ongeldig")
                    lcd.write_message("datum ongeldig", 0X80)
                    lcd.write_message("herscan barcode", 0xC0)
                    print(ex)

        except Exception as ex:
            print(ex)


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
        time.sleep(10)
        # Checken voor open en dicht soon...


def leesTemperatuur():
    while True:
        lees = TemperatuurClass(temperatuurSensor)
        socketio.emit('B2F_temperatuur', {
            'temperatuur': lees.leesTemp()}, broadcast=True)
        return lees.leesTemp()


def meetTemperatuur():
    while True:
        huidigTemp = TemperatuurClass(temperatuurSensor)
        return huidigTemp.meetTemp()


def keypadInputDoorgeven():
    uitvoer = leesKeypad()
    return uitvoer


def leesKeypad():
    while True:
        key = clKeypad(rijKeypad, kolumKeypad)
        toets = None
        if toets == None:
            toets = key.vangToets()
            if toets != None:
                print(toets)
                if toets == "#":
                    DataRepository.write_keypad(12)
                elif toets == "*":
                    DataRepository.write_keypad(10)
                else:
                    DataRepository.write_keypad(toets)
                return toets
            else:
                return None


def leesHistoriek():
    while True:
        hist = DataRepository.read_historiek()
        socketio.emit("B2F_history", hist, broadcast=True)
        time.sleep(5)


def start():
    pass


# Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@ socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


# API ENDPOINTS
endpoint = '/api/v1'


@ app.route(endpoint + '/historiek/', methods=['GET'])
def get_histo():
    if request.method == 'GET':
        hist = DataRepository.read_historiek()
        return jsonify(historiek=hist), 200


@ app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@ socketio.on('connect')
def initial_connection():
    print('A new client connect')
    data = DataRepository.geef_alle_producten()
    socketio.emit("B2F_connected", data)
    # # Send to the client!


@socketio.on("F2B_add-product")
def add(data):
    print('new product')
    try:
        d = datetime.strptime(data["datum"], '%Y-%m-%d').date()
        huidigeDatum = date.today()
        verschil = d-huidigeDatum
        print(verschil.days)
        voegtoe = DataRepository.add_product_by_web(
            data["naam"], data["datum"], int(verschil.days), int(data["aantal"]), data['barcode'])
        if voegtoe == -1:
            print("Deze product is al aanwezig")
            socketio.emit("B2F_alAanwezig", {
                          "aanwezig": "-1"})
        else:
            print("nieuwe product ingevoegd")
            socketio.emit("B2F_alAanwezig", voegtoe)
    except Exception as ex:
        print(ex)


@socketio.on("F2B_barcode")
def barOffline(invoer):
    if len(invoer) >= 13:
        print(invoer)
        barcodeInput(invoer)

# Thread


def start_thread():
    print("**** Starting THREAD ****")
    try:
        thread = threading.Thread(target=start, args=(), daemon=True)
        thread.start()
        temperatuur_thread()
        read_temperatuur_thread()
        oled_thread()
        lcd_thread()
        hist_thread()
        barcode_thread()
        MPU_thread()

    except Exception as ex:
        print(ex)


def oled_thread():
    try:
        print("**** OLED thread ****")
        thread = threading.Thread(target=showOled, args=(), daemon=True)
        thread.start()
    except Exception as ex:
        print(ex)


def barcode_thread():
    try:
        print("**** barcode thread ****")
        thread = threading.Thread(target=barcodeInput, args=(), daemon=True)
        thread.start()
    except Exception as ex:
        print(ex)


def hist_thread():
    try:
        print("**** HIST THREAD ****")
        thread = threading.Thread(target=leesHistoriek, args=(), daemon=True)
        thread.start()
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
    options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost/barcodeScanner.html")
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
