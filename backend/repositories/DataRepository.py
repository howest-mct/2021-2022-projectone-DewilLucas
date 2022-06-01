from .Database import Database


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

    def write_keypad(number):
        sql = "insert into Historiek(DeviceID,Waarde,Tijdstip) values(%s,%s,now())"
        param = [6, number]
        return Database.execute_sql(sql, param)

    def write_barcode(barcodeValue):
        try:
            sql = "insert into Product(Naam,EersteInvoeg,Barcode) values(%s,now(),%s)"
            params = ["Nog geen naam", barcodeValue]
            return Database.execute_sql(sql, params)
        except ValueError as ex:
            print(ex)
            return -1

    def zoekByBaarcode(barcode):
        sql = "SELECT idproduct from  Product where Barcode = %s"
        params = [barcode]
        return Database.get_one_row(sql, params)

    def add_product_in_inventory(id, datum, verschil, aantal):

        sql = "insert into ProductAanwezig(idProduct,invoerdatum,HoudbaarheidsDatum,AantalDagenResterend,aanwezig,aantal,idGebruiker) values(%s,now(),%s,%s,1)"
        param = [id, datum, verschil]
        return Database.execute_sql(sql, param)
