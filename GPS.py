from machine import UART, Pin
from micropyGPS import MicropyGPS
import time

gps = MicropyGPS(location_formatting='dd')
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

def gps_init(uart):
    uart.write(b'$PMTK104*37\r\n')
    uart.write(b'$PMTK314,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1*2C\r\n')
    uart.write(b'$PMTK220,1000*1F\r\n')
    uart.write(b'$PMTK397*0F\r\n')
    
if __name__ == '__main__':
    while True:
        if uart.any():
            line = uart.readline()
            if not line:
                continue
            
            try:
                text = line.decode('ascii', 'ignore').strip()
            except:
                print('ivalid data')
                continue
            
            if not text.startswith('$'):
                continue
            
            #continue 
            gps.update(text)

            if gps.latitude[0] != 0:  # has a fix
                print("Lat:", gps.latitude_string())
                print("Lon:", gps.longitude_string())
                print("Satellites:", gps.satellites_in_use)
                print("Time:", gps.timestamp)
                print("Date:", gps.date)
                print("-----")
            else:
                print('not fixed')
