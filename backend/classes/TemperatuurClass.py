from repositories.DataRepository import DataRepository
import time


class TemperatuurClass:
    def __init__(self, partempFile):
        self.tempsensor = partempFile
        self.sensorFile = open(self.tempsensor, 'r')

    def meetTemp(self):
        while True:
            vorigeTemp = DataRepository.read_temperatuur()

            self.sensorFile = open(self.tempsensor, 'r')
            for line in self.sensorFile:
                pos = line.find('t=')
                if pos > 0:
                    temperatuur = int(line.strip(
                        '\n')[pos+2:])/1000.0
                    if vorigeTemp["waarde"] == round(temperatuur, 2):
                        print("zelfde")
                    else:
                        insert_temp = DataRepository.write_temperatuur(
                            round((temperatuur), 2))
                        if insert_temp > 0:
                            uitvoer = f"temperatuur succesvol toegevoegd: {round(temperatuur, 2)}"
                            print(uitvoer)
            time.sleep(5)

    def leesTemp(self):
        while True:
            self.status = DataRepository.read_temperatuur()
            time.sleep(5)
            return self.status

    def sluitTemp(self):
        self.sensorFile.close()
