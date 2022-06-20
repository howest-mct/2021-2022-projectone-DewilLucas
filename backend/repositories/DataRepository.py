from .Database import Database
from datetime import datetime
import random
from datetime import datetime
from datetime import date
datumVandaag = datetime.today()


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_historiek():
        sql = "SELECT idMeting , DeviceID, Waarde,concat(Tijdstip)as `Tijdstip` FROM smartfridgeDB.Historiek WHERE DeviceID = 1 order by Tijdstip desc limit 20;"
        return Database.get_rows(sql)

    @staticmethod
    def write_temperatuur(temp):
        sql = "insert into Historiek(DeviceID,Waarde,Tijdstip) values(%s,%s,now())"
        params = [1, temp]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_temperatuur():
        sql = "SELECT waarde FROM Historiek where DeviceID = %s order by Tijdstip desc LIMIT 1;"
        param = [1]
        return Database.get_one_row(sql, param)

    @staticmethod
    def write_keypad(number):
        sql = "insert into Historiek(DeviceID,Waarde,Tijdstip) values(%s,%s,now())"
        param = [6, number]
        return Database.execute_sql(sql, param)

    @staticmethod
    def write_barcode(barcodeValue):
        try:
            sql = "insert into Product(Naam,EersteInvoeg,Barcode) values(%s,now(),%s)"
            params = ["Nog geen naam", barcodeValue]
            return Database.execute_sql(sql, params)
        except ValueError as ex:
            print(ex)
            return -1

    @staticmethod
    def zoekByBaarcode(barcode):
        sql = "SELECT idproduct from  Product where Barcode = %s"
        params = [barcode]
        return Database.get_one_row(sql, params)

    @staticmethod
    def add_product_in_inventory(id, datum, verschil, aantal):

        sql = "insert into ProductAanwezig(idProduct,invoerdatum,HoudbaarheidsDatum,AantalDagenResterend,aanwezig,aantal,idGebruiker) values(%s,now(),%s,%s,1,%s,%s)"
        param = [id, datum, verschil, aantal, 1]
        return Database.execute_sql(sql, param)

    @staticmethod
    def write_scan_history(barcode):
        sql = "insert into Historiek(DeviceID,Waarde,Tijdstip) values(%s,%s,now())"
        params = [2, barcode]
        return Database.execute_sql(sql, params)

    @staticmethod
    def aantal_aanwezigeproducten():
        sql = "SELECT sum(Aantal) as `totaalAanwezig` FROM smartfridgeDB.ProductAanwezig where aanwezig =%s;"
        param = [1]
        return Database.get_one_row(sql, param)

    @staticmethod
    def geef_alle_producten():
        sql = "SELECT p.Afbeelding, pa.idAanwezig,pa.idproduct,p.Naam,concat(pa.HoudbaarheidsDatum) as `HoudbaarheidsDatum`,pa.aantal from smartfridgeDB.ProductAanwezig pa join smartfridgeDB.Product p on p.idproduct = pa.idProduct where pa.aanwezig = %s order by `HoudbaarheidsDatum` asc;"
        param = [1]
        return Database.get_rows(sql, param)

    @staticmethod
    def add_product_by_web(naam, datum, verschil, aantal, barcode, afbeelding):
        sql3 = "SELECT idproduct from  smartfridgeDB.Product where naam = %s AND Barcode = %s"
        paraamA = [naam, barcode]
        test1 = Database.get_one_row(sql3, paraamA)
        if test1 == -1 or test1 == None:
            sql1 = "insert into Product(Naam,Eersteinvoeg,Barcode,Afbeelding) values(%s,now(),%s,%s)"
            param = [naam, barcode, afbeelding]
            Database.execute_sql(sql1, param)

            sql2 = "SELECT idproduct from  smartfridgeDB.Product where naam = %s AND Barcode = %s"
            paraam = [naam, barcode]
            uitvoer = Database.get_one_row(sql2, paraam)
            print(uitvoer)
            sql = "insert into ProductAanwezig(idproduct,invoerdatum,HoudbaarheidsDatum,AantalDagenResterend,aanwezig,aantal,idGebruiker) values(%s,now(),%s,%s,1,%s,%s)"
            params = [uitvoer['idproduct'], datum, verschil, aantal, 1]
            return Database.execute_sql(sql, params)
        else:
            sql4 = "SELECT idproduct from  smartfridgeDB.Product where naam = %s and Barcode = %s"
            paraam2 = [naam, barcode]
            uitvoer = Database.get_one_row(sql4, paraam2)
            print(uitvoer)
            sqlCheck = "SELECT idproduct,concat(HoudbaarheidsDatum) as `HoudbaarheidsDatum`,Aantal FROM ProductAanwezig WHERE idproduct = %s and HoudbaarheidsDatum =%s and aanwezig =1"
            param = [uitvoer['idproduct'], datum]
            uitvoerCheck = Database.get_one_row(sqlCheck, param)
            print(uitvoerCheck)
            if uitvoerCheck != -1:
                if uitvoerCheck['HoudbaarheidsDatum'] == datum and uitvoerCheck['Aantal'] == aantal:
                    print("al aanwezig")
                    return -1
            else:
                sql = "insert into ProductAanwezig(idproduct,invoerdatum,HoudbaarheidsDatum,AantalDagenResterend,aanwezig,aantal,idGebruiker) values(%s,now(),%s,%s,1,%s,%s)"
                params = [uitvoer['idproduct'], datum, verschil, aantal, 1]
                return Database.execute_sql(sql, params)

    @staticmethod
    def zoek_for_delete_by_barcode(barcode):
        sql1 = "SELECT idproduct FROM smartfridgeDB.Product WHERE barcode = %s;"
        param = [barcode]
        idtjen = Database.get_one_row(sql1, param)
        sql2 = "SELECT idProduct,HoudbaarheidsDatum,aantal FROM smartfridgeDB.ProductAanwezig WHERE idProduct = %s and aanwezig=1 order by HoudbaarheidsDatum asc LIMIT 1"
        id = [idtjen['idproduct']]
        test = Database.get_one_row(sql2, id)
        return test

    @staticmethod
    def delete_Product(id, datum):
        sql = "UPDATE smartfridgeDB.ProductAanwezig set aanwezig = 0, aantal = 0 WHERe idProduct = %s and houdbaarheidsdatum = %s"
        param = [id, datum]
        return Database.execute_sql(sql, param)

    @staticmethod
    def update_Product(verschil, id, datum):
        sql = "UPDATE smartfridgeDB.ProductAanwezig set aantal = %s WHERe idProduct = %s and houdbaarheidsdatum = %s"
        param = [verschil, id, datum]
        return Database.execute_sql(sql, param)

    @staticmethod
    def zoekbyAanwezigId(id):
        sql = "SELECT p.Naam,p.Barcode, pa.idProduct, concat(pa.HoudbaarheidsDatum) as `HoudbaarheidsDatum`, pa.Aantal,p.Afbeelding FROM smartfridgeDB.ProductAanwezig as pa join Product as p on pa.idProduct = p.idProduct where pa.idAanwezig = %s"
        param = [id]
        return Database.get_one_row(sql, param)

    @staticmethod
    def update_by_website_product(aanwezigID, naam, datum, aantal, barcode, verschil, afbeelding):
        sql = "SELECT p.Naam,p.Barcode, pa.idProduct FROM smartfridgeDB.ProductAanwezig as pa join Product as p on pa.idProduct = p.idProduct where pa.idAanwezig = %s"
        param = [aanwezigID]
        data = Database.get_one_row(sql, param)
        print(data['idProduct'])
        sql2 = "UPDATE smartfridgeDB.Product p  join smartfridgeDB.ProductAanwezig pa ON p.idproduct = pa.idProduct SET p.Naam = %s,pa.HoudbaarheidsDatum = %s,pa.aantal = %s,p.barcode = %s,pa.AantalDagenResterend = %s,p.Afbeelding=%s   where p.idProduct = %s and pa.idAanwezig = %s"
        param2 = [naam, datum, aantal, barcode,
                  verschil, afbeelding, data['idProduct'], aanwezigID]
        return Database.execute_sql(sql2, param2)

    @staticmethod
    def delete_by_website(id):
        sql = "DELETE FROM  smartfridgeDB.ProductAanwezig WHERE idAanwezig = %s"
        param = [id]
        return Database.execute_sql(sql, param)

    @staticmethod
    def user_login(mail, passwoord):
        sql = "SELECT idgebruiker,Naam,voornaam,`E-mail`,Passwoord, concat(LaatsteLog) FROM smartfridgeDB.Gebruiker WHERE `E-mail` = %s and Passwoord = %s;"
        param = [mail, passwoord]
        try:
            zoek = Database.get_one_row(sql, param)
            updateSql = "UPDATE smartfridgeDB.Gebruiker  SET LaatsteLog = now() WHERE `E-mail` = %s and Passwoord = %s"
            param2 = [mail, passwoord]
            Database.execute_sql(updateSql, param2)
            return zoek
        except Exception as ex:
            print("Gebruiker niet gevonden")
            return -1

    @staticmethod
    def update_user(id, naam, voornaam, email, pwd):
        sql = "UPDATE smartfridgeDB.Gebruiker SET Naam = %s,voornaam = %s,`E-mail`=%s,Passwoord = %s WHERE idgebruiker = %s"
        param = [naam, voornaam, email, pwd, id]
        try:
            up = Database.execute_sql(sql, param)
            return up
        except Exception as ex:
            print(ex)
            return -1

    @staticmethod
    def updateDatums():
        sqlZoekalles = "SELECT idAanwezig,concat(HoudbaarheidsDatum) as HoudbaarheidsDatum from  smartfridgeDB.ProductAanwezig"
        alleDatums = Database.get_rows(sqlZoekalles)
        for datum in alleDatums:
            id = datum['idAanwezig']
            gevonden = datetime.strptime(
                datum['HoudbaarheidsDatum'], '%Y-%m-%d')
            verschil = gevonden - datumVandaag
            sql = "UPDATE smartfridgeDB.ProductAanwezig SET AantalDagenResterend=%s where idAanwezig = %s"
            param = [int(verschil.days), id]
            Database.execute_sql(sql, param)

    @staticmethod
    def geefOverdatums():
        lstOverDatum = []
        sql = "SELECT p.Naam, pa.idAanwezig, concat(pa.HoudbaarheidsDatum) as HoudbaarheidsDatum from smartfridgeDB.ProductAanwezig pa join Product p on pa.idProduct = p.idproduct WHERE pa.AantalDagenResterend <= 0 order by pa.AantalDagenResterend asc"
        over = Database.get_rows(sql)
        for product in over:
            lstOverDatum.append(product)
        return lstOverDatum

    @staticmethod
    def get_mails():
        pass

    @staticmethod
    def add_user(naam, voornaam, email, hex_dig):
        try:
            sql = "insert into smartfridgeDB.Gebruiker(Naam,voornaam,`E-mail`,Passwoord) values(%s,%s,%s,%s)"
            params = [naam, voornaam, email, hex_dig]
            add = Database.execute_sql(sql, params)
            return add
        except Exception as ex:
            return -1

    @staticmethod
    def delete_user(id):
        try:
            sql = "Delete from smartfridgeDB.Gebruiker where idgebruiker = %s"
            param = [id]
            delete = Database.execute_sql(sql, param)
            return delete
        except Exception as ex:
            print(ex)
            return -1

    @staticmethod
    def geefmails():
        try:
            sql = "SELECT `E-mail` FROM smartfridgeDB.Gebruiker;"
            mails = Database.get_rows(sql)
            return mails
        except Exception as ex:
            print(ex)
            return -1
