from machine import Pin, I2C, UART
from utime import sleep, time_ns
from bmp_driver import *
from GPS import *

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
gps = MicropyGPS(location_formatting='dd')
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

w_file = open('weatherdata.txt','w')
g_file = open('gpsdata.txt','w')

print(i2c.scan())

bmp280 = bmp_init(i2c)
gps_init(uart)

t_last = time_ns()
while True:
    
    t = time_ns()
    if t - t_last >= 1E9:
        t_last = t
        weather = bmp_read(bmp280)
        w_str = '\n'+str(weather['t']) + ', ' + str(weather['p']) + ', ' + str(weather['a']) 
        w_file.write(w_str)
    
    if uart.any():
        line = uart.read(5)
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
            string += ', Vel: '+gps.speed_string()
            string += ', Dir: '+str(gps.compass_direction)
            string += ', Dat: '+gps.date_string(formatting='s_dmy')
            string += ', Time:'+str(gps.timestamp)
            g_file.write(string)
        else:
            g_file.write('\n not fixed')
        