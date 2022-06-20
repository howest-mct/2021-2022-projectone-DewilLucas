import time
from RPi import GPIO
import threading
import sys
from subprocess import check_output
import os
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request, render_template, redirect
from repositories.DataRepository import DataRepository
#from classes.mpuClass import MPU6050
from classes.keypadClass import clKeypad
from selenium import webdriver
from classes.TemperatuurClass import TemperatuurClass
from classes.lcdClass import Lcd
from classes.OLEDCLass import OLED
from datetime import datetime
from datetime import date
import hashlib
from classes.clEmail import emailPy
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# Variables
temperatuurSensor = '/sys/bus/w1/devices/28-0417819474ff/w1_slave'
#mpu = MPU6050(0x68)
rijKeypad = [9, 6, 22, 27]
kolumKeypad = [24, 12, 5]
button = 18
lcdPins = [23, 26, 19, 13]
E = 20
RS = 21
lcd = Lcd(E, RS, lcdPins)
oled = OLED(128, 64, 5)
lees = TemperatuurClass(temperatuurSensor)
user = -1
tellerAfzetten = 0
histMode = "seconds"
# Code voor Hardware


def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button, GPIO.FALLING, pushed, 200)


def pushed(knop):
    global tellerAfzetten
    print("**** Read keypad THREAD *****")
    thread = threading.Thread(
        target=leesKeypad, args=(), daemon=True)
    thread.start()
    uit = []
    lcd.init_LCD()
    lcd.write_message("Want to close?:#", 0X80)
    lcd.write_message("Don't close?:*", 0XC0)
    while len(uit) != 1:
        inofUit = leesKeypad()
        if inofUit == "#" or inofUit == "*":
            uit.append(inofUit)
        tellerAfzetten += 1
        print(tellerAfzetten)
        if tellerAfzetten == 5000:
            uit.append("*")
            tellerAfzetten = 0
    if uit[0] == "#":
        print("TURNED OFF")
        lcd.write_message("TURNED OFF", 0x80)
        time.sleep(1)
        lcd.init_LCD()
        oled.Clear_oled()
        os.system("sudo shutdown -h now")
        sys.exit()
        # quits the code
    else:
        tellerAfzetten = 0
        schrijfLCD()


def reboot():
    while True:
        datumVandaag = datetime.now()
        if datumVandaag.hour == 0 and datumVandaag.minute == 0 and datumVandaag.second == 0:
            print("UPDATE")
            DataRepository.updateDatums()
            mails = DataRepository.geefmails()
            overdatum = DataRepository.geefOverdatums()
            for email in mails:
                print(email)
                mail = emailPy(overdatum, email['E-mail'])
        else:
            pass


def geefAantal():
    while True:
        totaalAanwezig = DataRepository.aantal_aanwezigeproducten()
        if totaalAanwezig == -1:
            print(totaalAanwezig)
            return "Geen aanwezige producten"
        else:
            print(totaalAanwezig['totaalAanwezig'])
            getal = int(totaalAanwezig['totaalAanwezig'])
            socketio.emit(
                "B2F_aantal", {'aantal': getal}, broadcast=True)
            return f"Number of product:{totaalAanwezig['totaalAanwezig']}"


def showOled():
    while True:
        huidigeTemp = leesTemperatuur()
        print(huidigeTemp["waarde"])

        aanwezig = geefAantal()
        socketio.emit('B2F_temperatuur', {
            'temperatuur': huidigeTemp}, broadcast=True)
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
            thread = threading.Thread(
                target=leesKeypad, args=(), daemon=True)
            thread.start()
            uit = []
            lcd.init_LCD()
            lcd.write_message("Add product:#", 0X80)
            lcd.write_message("Delete product:*", 0xC0)
            while len(uit) != 1:
                inofUit = leesKeypad()
                if inofUit == "#" or inofUit == "*":
                    uit.append(inofUit)

            else:
                lcd.init_LCD()
                DataRepository.write_scan_history(barcode)
                zoek = DataRepository.zoekByBaarcode(barcode)
                if zoek == -1:
                    DataRepository.write_barcode(barcode)
                    lcd.write_message("Change the name", 0X80)
                    lcd.write_message("On the web app", 0xC0)
                    print("nieuwe product ingevoegd")
                    time.sleep(2)
                    lcd.init_LCD()
                    zoek = DataRepository.zoekByBaarcode(barcode)
                if uit[0] == "#":
                    lcd.write_message("Expiry date", 0x80)
                    lstDatum = []

                    while len(lstDatum) != 8:
                        waarde = leesKeypad()
                        if waarde == None or waarde == "#":
                            pass
                        elif waarde == "*":
                            lcd.init_LCD()
                            lcd.write_message("STOPPED", 0x80)
                            time.sleep(2)
                            schrijfLCD()
                            break
                        else:
                            lstDatum.append(waarde)
                            strDatum = str(lstDatum)
                            newStrdatum = converteerListNaarStr(strDatum)
                            finalString = f"{newStrdatum[:2]}-{newStrdatum[2:4]}-{newStrdatum[4:len(newStrdatum)]}"
                            lcd.write_message(finalString, 0XC0)
                    else:
                        eersteGetal = str(lstDatum[0]) + str(lstDatum[1])
                        tweedeGetal = str(lstDatum[2]) + str(lstDatum[3])
                        jaartal = str(
                            lstDatum[4])+str(lstDatum[5])+str(lstDatum[6]) + str(lstDatum[7])
                        datumke = f"{jaartal}-{tweedeGetal}-{eersteGetal}"
                        try:
                            d = datetime.strptime(datumke, '%Y-%m-%d').date()
                            huidigeDatum = date.today()
                            verschil = d-huidigeDatum
                            if verschil.days <= 0:
                                raise(Exception)
                            else:
                                lcd.init_LCD()
                                lcd.write_message("How much?", 0x80)
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
                                lcd.write_message("This is a...", 0x80)
                                lcd.write_message("Succes! :)", 0XC0)
                                time.sleep(3)
                                schrijfLCD()
                        except Exception as ex:
                            print("datum ongeldig")
                            lcd.write_message("date invalid", 0X80)
                            lcd.write_message("rescan barcode", 0xC0)
                            print(ex)
                else:
                    try:
                        zoek_delete = DataRepository.zoek_for_delete_by_barcode(
                            barcode)
                        print(zoek_delete)
                        totaalAantal = zoek_delete['aantal']
                        lcd.write_message("How much?", 0x80)
                        lcd.write_message(">", 0xC0)
                        aantalVerwijderen = []
                        vw = ""
                        final2 = ""
                        while vw != '#':
                            vw = leesKeypad()
                            if vw == "#":
                                if int(final2) > totaalAantal:
                                    vw = ""
                                    aantalVerwijderen = []
                                    final2 = ">"
                                    lcd.write_message("TOO MUCH!", 0XC0)
                                    time.sleep(2)
                                    lcd.write_message(final2, 0XC0)
                            elif vw == "*":
                                lcd.init_LCD()
                                lcd.write_message("STOPPED", 0x80)
                                time.sleep(2)
                                schrijfLCD()
                                break
                            elif vw == None:
                                pass
                            else:
                                aantalVerwijderen.append(vw)
                                strVerwijderen = str(aantalVerwijderen)
                                convStrAantal = converteerListNaarStr(
                                    strVerwijderen)

                                final2 = f"{convStrAantal}"
                                lcd.write_message(final2, 0XC0)
                        else:
                            try:
                                verschilVerwijdern = totaalAantal - int(final2)
                                print(verschilVerwijdern)
                                if verschilVerwijdern == 0:
                                    DataRepository.delete_Product(
                                        zoek_delete['idProduct'], zoek_delete['HoudbaarheidsDatum'])
                                else:
                                    DataRepository.update_Product(
                                        verschilVerwijdern, zoek_delete['idProduct'], zoek_delete['HoudbaarheidsDatum'])
                                lcd.init_LCD()
                                lcd.write_message("DELETE...", 0x80)
                                lcd.write_message("SUCCES!", 0xC0)
                                time.sleep(3)
                                schrijfLCD()
                            except Exception as ex:
                                print(ex)

                    except Exception as ex:
                        print(ex)

        except Exception as ex:
            print(ex)


def schrijfLCD():
    lcd.init_LCD()  # kuis het eerst op
    ips = check_output(
        ['hostname', '--all-ip-addresses']).split()
    # Eerste ip die binnenkomt aka de ip van de ethernetpoort
    eth = ips[0]
    # wlan = ips[1]  # de ip van de raspberry
    lcd.write_message(f"{eth.decode()}", 0x80)  # 0x80 is lijn 1 van de LCD
    # lcd.write_message(f"{wlan.decode()}", 0xC0)  # 0xC0 is lijn 2 van de LCD


# def leesMPU():
 #   while True:
  #      mpu.printAlles()
   #     time.sleep(10)
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
        global histMode
        #hist = DataRepository.read_historiek()
        #socketio.emit("B2F_history", hist, broadcast=True)
        if histMode == "day":
            uitvoer = DataRepository.read_by_day()
        if histMode == "hour":
            uitvoer = DataRepository.read_by_hour()
        if histMode == "minute":
            uitvoer = DataRepository.read_by_minute()
        if histMode == 'seconds':
            uitvoer = DataRepository.read_historiek()
        socketio.emit("B2F_hist", uitvoer)
        time.sleep(1)


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
    return render_template("index.html")


@ socketio.on('connect')
def initial_connection():
    print('A new client connect')
    data = DataRepository.geef_alle_producten()
    socketio.emit("B2F_connected", data)
    DataRepository.geefOverdatums()
    socketio.emit('B2F_temperatuur', {
                  'temperatuur': leesTemperatuur()}, broadcast=True)

    # # Send to the client!


@socketio.on("F2B_historyChange")
def changehist(data):
    global histMode
    histMode = data


@ socketio.on("F2B_add_user")
def add_user(data):
    naam = data["naam"]
    voornaam = data['voornaam']
    email = data['email']
    passwoordSalted = f"{email}s@lt#{data['passwoord']}#tl@s"
    print(passwoordSalted)
    hash_object = hashlib.sha512(passwoordSalted.encode())
    hex_dig = hash_object.hexdigest()
    voeg = DataRepository.add_user(naam, voornaam, email, hex_dig)
    if voeg == -1:
        pass
    else:
        print("succes!")


@ socketio.on("F2B_gebruiker")
def connection(data):
    email = data['mail']
    passwoordSalted = f"{email}s@lt#{data['passwoord']}#tl@s"
    hash_object = hashlib.sha512(passwoordSalted.encode())
    hex_dig = hash_object.hexdigest()
    login = DataRepository.user_login(email, hex_dig)
    print(login)
    global user
    user = login


@ socketio.on("F2B_delete_account")
def deleteUser(data):
    try:
        delete = DataRepository.delete_user(data['idgebruiker'])
        if delete != -1:
            user = -1
            socketio.emit("B2F_user_delete", user)
    except Exception as ex:
        print(ex)


@ socketio.on("F2B_loadPage")
def loadpage(data):
    print(data)
    if data == 1:
        socketio.emit("B2F_user", user)


@ socketio.on("F2B_account")
def showAccount(data):
    if data == 1:
        socketio.emit("B2F_account", user)


@ socketio.on("F2B_update_user")
def updateAccount(data):
    print(data)
    id = data['id']
    naam = data["naam"]
    voornaam = data['voornaam']
    email = data['email']
    hex_dig = ""
    global user
    print(user)
    if user['Passwoord'] == data['passwoord']:
        hex_dig = user['Passwoord']
        print(hex_dig)
    else:
        passwoordSalted = f"{email}s@lt#{data['passwoord']}#tl@s"
        hash_object = hashlib.sha512(passwoordSalted.encode())
        hex_dig = hash_object.hexdigest()
        print(hex_dig)

    updateuser = DataRepository.update_user(
        id, naam, voornaam, email, hex_dig)
    if updateuser != -1:
        user = updateuser
        socketio.emit("B2F_updated_user", updateuser)
    else:
        socketio.emit("B2F_updated_user", user)


@ socketio.on("F2B_delete_product")
def delete_product(id):
    print("Start delete")
    verwijder = DataRepository.delete_by_website(id)
    socketio.emit("B2F_deleted", verwijder)


@ socketio.on('F2B_edit')
def edit(data):
    global aanwezigID
    global uitv

    aanwezigID = data
    uitv = DataRepository.zoekbyAanwezigId(data)
    if uitv != None or uitv != -1:
        socketio.emit("B2F_edit", uitv)
        print(uitv)
    else:
        print("Geen data gevonden")


@ socketio.on("F2B_add-product")
def add(data):
    print('new product')
    try:
        print(data)
        d = datetime.strptime(data["datum"], '%Y-%m-%d').date()
        huidigeDatum = date.today()
        verschil = d-huidigeDatum
        print(verschil.days)
        voegtoe = DataRepository.add_product_by_web(
            data["naam"], data["datum"], int(verschil.days), int(data["aantal"]), data['barcode'], data["foto"])
        if voegtoe == -1:
            print("Deze product is al aanwezig")
            socketio.emit("B2F_alAanwezig", {
                          "aanwezig": "-1"})
        else:
            print("nieuwe product ingevoegd")
            socketio.emit("B2F_alAanwezig", voegtoe)
    except Exception as ex:
        print(ex)


@ socketio.on("F2B_edit_product")
def update_product(data):
    try:
        print(data)
        d = datetime.strptime(data["datum"], '%Y-%m-%d').date()
        huidigeDatum = date.today()
        verschil = d-huidigeDatum
        print(verschil)
        if aanwezigID != None or aanwezigID != -1:
            DataRepository.update_by_website_product(
                aanwezigID, data["naam"], data['datum'], data['aantal'], data["barcode"], int(verschil.days), data["foto"])
        else:
            print("Geen data gevonden")

    except Exception as ex:
        print(ex)


@socketio.on("F2B_shutdown")
def shutdown_by_web(json):
    print("TURNED OFF")
    os.system("sudo shutdown -h now")
    sys.exit()
    # quits the code


@ socketio.on("F2B_barcode")
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
        # MPU_thread()
        update_thread()
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


def update_thread():
    print("**** UPDATE THREAD ****")
    try:
        thread = threading.Thread(target=reboot, args=(), daemon=True)
        thread.start()
    except Exception as ex:
        print(ex)


# def MPU_thread():
#    print("**** MPU THREAD ****")
#    try:
#        thread = threading.Thread(target=leesMPU, args=(), daemon=True)
#        thread.start()
#    except Exception as ex:
#        print(ex)


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
    # options.add_argument("disable-infobars")
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
        DataRepository.updateDatums()

        setup_gpio()
        start_thread()
        start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        # mpu.sluit()
        temp.sluitTemp()
        lcd.init_LCD()
        GPIO.cleanup()
