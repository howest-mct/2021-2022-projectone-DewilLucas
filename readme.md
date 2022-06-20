# Project One - SmartFridge

![white logo](https://user-images.githubusercontent.com/91437297/174548596-aaea518d-f75b-499e-823d-c50895515a07.png)

## Introduction
As a student, I often had the problem that too much food went to the bin because I didn't really have an inventory of what was in my fridge.

Which is a big issue because I, as a student, do not have much money to buy food every time.

The environment is also something that is very important to me, did you know that a third to half of all the food produced is lost or wasted and causes about 8% of global greenhouse gas emissions?



At the end of this project, I want to have achieved the following:

- I want to see what I should eat first
- Be able to follow up on an inventory remotely
- Monitor the current temperature, so I can see if it is too high (or too low) for my food
- Get a notification of what is already past due and what is about to go past due
- I want to see when the fridge is open
- I am sharing this with you so that you too can easily do your bit to preserve our environment and make your bills smaller. (And secretly for the smell of food that has been sitting in your fridge for a long time ;))


## Sensors and actuators used for this project
### Main computing unit:

- Raspberry Pi 4
- 16Go SD card


### Electronics:

- T-Type GPIO Adapter
- Wiring cables
- Breadboard
- Breadboard power adapter 3.3V/5V
- Resistors
### Sensors:

- 3X4 flexible matrix keypad
- USB Laser barcode scanner
- Waterproof 1-wire temperature sensor (ds18b20)
### Actuators:
- 16X2 LCD Display 
- I2C OLED DISPLAY
## Prepare the Raspberry Pi

### Dowload the image
- Download the Raspberry Pi os, the desktop version from [here](https://www.raspberrypi.com/software/operating-systems/)
> If you don't know how to install an image, [here is a tutorial](https://www.youtube.com/watch?v=cOYTE0TjQL8)
### Once the image is downloaded and installed
- Use an ssh client to login e.g. [putty](https://putty.org/) or [vnc](https://www.bing.com/search?q=vnc&cvid=bb4314aa5fec4011a0145ee18f13425b&aqs=edge..69i57j0l8.590j0j4&FORM=ANAB01&PC=U531), the ip address to login is 169.254.10.1 and the port is 22 connection type is ssh
- On the first login the **user** is **pi** and the **password** is **raspberry**
- For the warning message click on yes
> It is always a good idea to create a user and change the password [here is a tutorial](https://www.youtube.com/watch?v=xAV4p7KDr4Q)

### Once you are logged in
1. Type sudo ```raspi-config```in the terminal
2. In the menu choose (6) **Advanced** > (1) **Expand Filesystem**
3. Then reboot the raspberry pi with command :
```
sudo reboot now
```
### After the reboot
1. Go back to:
```
sudo raspi-config
```
This time we go to (3) Interfaces
1. Enable the **one wire bus** (i7)
2. Enable the **I2C(i5) bus**
3. Enable the **SPI(i4) bus**
4. Enable the **vnc(i3)** it will make it easier if there are issues in the terminal
5. Reboot the raspberry pi with command:
```
sudo reboot now
```
### Connect the raspberry pi to the wifi
1. Get administrator rights:
```
sudo -i
```
2. Once your administrator type:
```
wpa_passphrase <your_SSID@Home> <your_wifi password> >>/etc/wpa_supplicant/wpa_supplicant.conf
```
> Replace <your_SSID@Home> with the name of your home network and <your_wifi password> with the corresponding password.
3. Type now:
```
wpa_cli -i wlan0 reconfigure
```
> To reload your wireless network card in the RasPi.

4. A test to see if you are connected to the internet: 
```
ping www.google.com
```
--> If you see this you're connected to the wifi:
```
PING www.google.com(ams15s41-in-x04.1e100.net (2a00:1450:400e:802::2004)) 56 data bytes
64 bytes from ams16s21-in-x04.1e100.net (2a00:1450:400e:802::2004): icmp_seq=1 ttl=113 time=23.2 ms
64 bytes from ams16s21-in-x04.1e100.net (2a00:1450:400e:802::2004): icmp_seq=2 ttl=113 time=22.2 ms
64 bytes from ams16s21-in-x04.1e100.net (2a00:1450:400e:802::2004): icmp_seq=3 ttl=113 time=23.5 ms
--- www.google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
```
5. Update the Raspberry Pi
```sudo apt update``` to check which updates are available.

```sudo apt upgrade -y``` to install the available updates.

### Install Apache server
```
sudo apt install apache2 -y
```
### Install mariaDB
```
sudo apt install mariadb-server mariadb-client -y
```
### Securing MariaDB
```
mysql_secure_installation
```
- First you will be asked to enter the current root password for MariaDB. As there is none yet, just press ```Enter``` here.
- Next, you can change the password. Choose a password you can remember for sure!
- The next step is to delete anonymous users. Choose ```y``` here
- Prohibit root from logging in remotely. Choose ```y``` here.
- Then remove test database and access? Choose ```y```.
- Finally, reload privilege databases: ```y```
### Create MariaDB User
- Next, we configure the user 'choose a name' with a password on the MariaDB server.
- ```mysql -u root -p``` to access the MariaDB server
```grant all on *.* to 'yourname'@'localhost' identified by 'yourpassword'; 
grant grant option on *.* to 'yourname'@'localhost';
flush privileges;
exit;
```
- Creates a new user with password who gets rights to all databases.
- flush privileges Reload privileges
- exit Exit from the MariaDB server
### Install the library's and python3
```
sudo pip install flask-cors
sudo pip install flask-socketio
sudo pip install simple-websocket
sudo pip install mysql-connector-python
sudo pip install gevent
sudo pip install gevent-websocket
sudo pip install selenium
sudo apt install chromium-chromedriver
sudo apt install python3-dev python3-pip
```
### After installation reboot the raspberry
```
sudo reboot
```
### Install the code
```
git clone https://github.com/howest-mct/2021-2022-projectone-DewilLucas.git
```

## Database
- Start mysqlworkbench on your laptop
- Make a new connection.
- Connection Method:Standard TCP/IP over SSH.
- SSH Hostname: ```169.254.10.1```
- SSH Username: pi(or the username you gave it)
- SSH Password: raspberry(or the password you gave it)
- MySQL Hostname: ```127.0.0.1```
- MySQL Server Port: ```3306```
- Username: yourname (the name you gave in the database)
- Password: yourpassword(the password you gave in the database)
> You can import the database from [here](https://github.com/howest-mct/2021-2022-projectone-DewilLucas/blob/master/database-export/dump_smartfridge.sql)

# Run it for the first time
```sudo /bin/python3 /backend/app.py```
### Start it up automatically
```nano /etc/systemd/system/smartfridge.service```
- then type in it:
```
[Unit]
Description=smartFridge
After=network.target
[Service]
ExecStart=/usr/bin/python3 -u /home/student/2021-2022-projectone-DewilLucas/backend/app.py
WorkingDirectory=/home/student/2021-2022-projectone-DewilLucas/backend
StandardOutput=inherit
StandardError=inherit
Restart=always
User=student
[Install]
WantedBy=multi-user.target
```
# **!!!Save the file!!!**
```CTRL X --> y ENTER```
### Copy the service
```
sudo smartfridge.service /etc/systemd/system/smartfridge.service
```
### Test
- You can test it by type in;

```systemctl start smartfridge.service```
- You can also stop it:
```systemctl stop smartfridge.service```
- The automatic start

```sudo systemctl enable smartfridge.service```
## About the code
### Technologies - backend
- Python
- Threading library (build in)
- socketio
- mysqlconnector
- ssl
- smtplib
- EmailMessage
- adafruit_ssd1306
### Technologies - front-end
- HTML 5
- CSS 3
- Javascript
- ApexCharts.js
- socketio
# Circuit diagram
You can find my [fritzing schematic here](https://github.com/howest-mct/2021-2022-projectone-DewilLucas/tree/master/fritzing_schema)
# Instructable
I have made an enclosure for this project, if you want to see how I made it you can [look at my instructable]()
