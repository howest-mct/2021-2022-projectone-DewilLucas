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
        sql = "SELECT * FROM Historiek;"
        return Database.get_rows(sql)

    @staticmethod
    def read_temperatuur():
        sql = "SELECT waarde FROM smartfridgeDB.Historiek where DeviceID = %s;"
        param = [1]
        return Database.get_one_row(sql, param)
