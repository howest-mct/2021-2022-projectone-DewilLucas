import time
sensor = '/sys/bus/w1/devices/28-22cfd2000900/w1_slave'

try:
    while True:

        sensorFile = open(sensor, 'r')
        for line in sensorFile:

            pos = line.find('t=')
            if pos > 0:
                temperatuurSensor = int(line.strip(
                    '\n')[pos+2:])/1000.0
                print(f'Het is {temperatuurSensor} °C')

        sensorFile.close()
        time.sleep(0.5)
except KeyboardInterrupt:
    print('Gestopt')
finally:
    print('einde code')
