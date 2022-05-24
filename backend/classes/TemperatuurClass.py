from repositories.DataRepository import DataRepository
import time
from RPi import GPIO


class TemperatuurClass:
    def __init__(self, partempFile):
        self.tempsensor = partempFile

    def meetTemp(self):
        while True:
            self.sensorFile = open(self.tempsensor, 'r')
            for line in self.sensorFile:
                pos = line.find('t=')
                if pos > 0:
                    temperatuur = int(line.strip(
                        '\n')[pos+2:])/1000.0
                    insert_temp = DataRepository.write_temperatuur(
                        round((temperatuur), 2))
                    if insert_temp > 0:
                        uitvoer = f"temperatuur succesvol toegevoegd: {round(temperatuur, 2)}"
                        print(uitvoer)
            time.sleep(5)

    def sluitTemp(self):
        self.sensorFile.close()
