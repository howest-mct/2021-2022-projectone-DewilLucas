import time
from smbus import SMBus

i2c = SMBus()
i2c.open(1)


class MPU6050:
    def __init__(self, adres):
        self.raw = []
        self.addres = adres
        self.setup()

    def setup(self):
        self.write_byte(0x1C, 0x00)
        self.write_byte(0x1B, 0x00)
        self.write_byte(0x6B, 0x01)

    def printAlles(self):
        print("***")
        print(f'Raw_data : {sum(self.raw, [])}')
        self.raw = []
        print(f'De temperatuur is {self.temperatuur()}°C')
        accel = self.read_accel()
        gyro = self.read_gyro()
        print(
            f'Accel: x={accel[0]}, y={accel[1]}, z={accel[2]}\nsom accelero: {sum(accel)}\nGyro: x={gyro[0]}°/ s, y={gyro[1]}°/ s, z={gyro[2]}°/ s')

    def temperatuur(self):
        invoer = self.__read_data(0x41, 2)
        return round(invoer[0] / 340 + 36.53, 2)

    def read_accel(self):
        values = self.__read_data(0x3B, 6)
        for i in range(len(values)):
            values[i] = round(values[i] / 16384, 2)
        return values

    def read_gyro(self):
        values = self.__read_data(0x43, 6)
        for i in range(len(values)):
            values[i] = round(values[i] / 250, 2)
        return values

    def write_byte(self, register, value):
        i2c.write_byte_data(self.addres, register, value)

    def __read_data(self, register, count):
        arr = i2c.read_i2c_block_data(self.addres, register, count)
        self.raw.append(arr)
        values = []
        for i in range(0, count, 2):
            byte = self.combine_bytes(arr[i], arr[i+1])
            values.append(byte)
        return values

    def sluit(self):
        i2c.close()

    @staticmethod
    def combine_bytes(msb, lsb):
        value = msb << 8 | lsb
        if value & 0x8000:
            value -= 2**16
        return value


if __name__ == "__main__":
    mpu = MPU6050(0x68)
    try:
        while True:
            mpu.printAlles()
            time.sleep(1)
    except KeyboardInterrupt:
        print('quitting')
    finally:
        mpu.sluit()
