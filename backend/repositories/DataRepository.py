from .Database import Database
from datetime import datetime
import random


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
        sql = "SELECT idMeting , DeviceID, Waarde,concat(Tijdstip)as `Tijdstip` FROM smartfridgeDB.Historiek order by Tijdstip desc;"
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
        sql = "SELECT pa.idAanwezig,p.idproduct,concat(pa.HoudbaarheidsDatum) as `houdbaarheidsdatum`,cast(sum(Aantal) as int) as `aantal`,p.Naam FROM smartfridgeDB.Product p join smartfridgeDB.ProductAanwezig pa on p.idproduct = pa.idProduct where pa.aanwezig = %s and pa.aantal>0 group by pa.houdbaarheidsdatum;"
        param = [1]
        return Database.get_rows(sql, param)

    @staticmethod
    def add_product_by_web(naam, datum, verschil, aantal, barcode):
        sql3 = "SELECT idproduct from  smartfridgeDB.Product where naam = %s AND Barcode = %s"
        paraamA = [naam, barcode]
        test1 = Database.get_one_row(sql3, paraamA)
        if test1 == -1 or test1 == None:
            sql1 = "insert into Product(Naam,Eersteinvoeg,Barcode) values(%s,now(),%s)"
            param = [naam, barcode]
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
            sqlCheck = "SELECT idproduct,concat(HoudbaarheidsDatum) as `HoudbaarheidsDatum`FROM ProductAanwezig WHERE idproduct = %s and HoudbaarheidsDatum =%s and aanwezig =1"
            param = [uitvoer['idproduct'], datum]
            uitvoerCheck = Database.get_one_row(sqlCheck, param)
            print(uitvoerCheck)
            print(uitvoerCheck['HoudbaarheidsDatum'])
            if uitvoerCheck['HoudbaarheidsDatum'] == datum:
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
        sql = "UPDATE smartfridgeDB.ProductAanwezig set aanwezig = 0,set aantal = 0 WHERe idProduct = %s and houdbaarheidsdatum = %s"
        param = [id, datum]
        return Database.execute_sql(sql, param)

    @staticmethod
    def update_Product(verschil, id, datum):
        sql = "UPDATE smartfridgeDB.ProductAanwezig set aantal = %s WHERe idProduct = %s and houdbaarheidsdatum = %s"
        param = [verschil, id, datum]
        return Database.execute_sql(sql, param)

    @staticmethod
    def zoekbyAanwezigId(id):
        sql = "SELECT p.Naam,p.Barcode, pa.idProduct, concat(pa.HoudbaarheidsDatum) as `HoudbaarheidsDatum`, pa.Aantal FROM smartfridgeDB.ProductAanwezig as pa join Product as p on pa.idProduct = p.idProduct where pa.idAanwezig = %s"
        param = [id]
        return Database.get_one_row(sql, param)

    @staticmethod
    def update_by_website_product(aanwezigID, naam, datum, aantal, barcode, verschil):
        sql = "SELECT p.Naam,p.Barcode, pa.idProduct FROM smartfridgeDB.ProductAanwezig as pa join Product as p on pa.idProduct = p.idProduct where pa.idAanwezig = %s"
        param = [aanwezigID]
        data = Database.get_one_row(sql, param)
        print(data['idProduct'])
        sql2 = "UPDATE smartfridgeDB.Product p  join smartfridgeDB.ProductAanwezig pa ON p.idproduct = pa.idProduct SET p.Naam = %s,pa.HoudbaarheidsDatum = %s,pa.aantal = %s,p.barcode = %s,pa.AantalDagenResterend = %s   where p.idProduct = %s and pa.idAanwezig = %s"
        param2 = [naam, datum, aantal, barcode,
                  verschil, data['idProduct'], aanwezigID]
        Database.execute_sql(sql2, param2)
