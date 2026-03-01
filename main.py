from machine import Pin, I2C, UART
from utime import sleep, time_ns
from bmp_driver import *
from GPS import *
from radio import *

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
spi = SPI(0, baudrate=5000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

gps = MicropyGPS(location_formatting='dd')

w_file = open('weatherdata.txt','w')
g_file = open('gpsdata.txt','w')
freq = 433E6

bmp280 = bmp_init(i2c)
gps_init(uart)
lora = radio_init(spi, freq)

t_last = time_ns()

string = ''
while True:
    
    t = time_ns()
    if t - t_last >= 1E9:
        t_last = t
        weather = bmp_read(bmp280)
        w_str = '\n'+str(weather['t']) + ', ' + str(weather['p']) + ', ' + str(weather['a']) 
        w_file.write(w_str)
        g_file.write(string)
        
        send(lora, w_str)
        send(lora, string)
        payload = receive(lora)
        if payload != '':
            print('payload received')
    
    if uart.any():
        line = uart.read(10)
        if not line:
            continue
        
        try:
            text = line.decode('ascii', 'ignore').strip()
        except:
            continue
        
        if not text.startswith('$'):
            continue
        
        #continue
        for i in range(len(text)):
            gps.update(text[i])
        
        if gps.latitude[0] != 0:  # has a fix
            string = '\n Lat: '+gps.latitude_string()
            string += ', Lon: '+gps.longitude_string()
        else:
            string = '\nNot Fixed'
    
        