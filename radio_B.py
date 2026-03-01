from time import sleep
from sx127x import *
from machine import SPI, Pin
import select, sys

def radio_init(spi, freq):
    
    lora = SX127x(spi=spi,
              pins={'ss' : Pin(17, Pin.OUT),
                    'reset':Pin(14, Pin.OUT),
                    'dio_0':Pin(15, Pin.IN)},
              parameters = {
            'frequency': freq, 
            'tx_power_level': 2, 
            'signal_bandwidth': 125E3,    
            'spreading_factor': 8, 
            'coding_rate': 5, 
            'preamble_length': 8,
            'implicit_header': False, 
            'sync_word': 0x12, 
            'enable_CRC': False,
            'invert_IQ': False,
            })
    
    return lora

def receive(lora):

    for _ in range(100):
        if lora.received_packet():
            print('something here')
            payload = lora.read_payload()
            print(payload)

def send(lora, msg):
    
    counter = 0
    print("LoRa Sender")

    while counter <= 2:
        payload = msg.format(counter)
        print("Sending packet: \n{}\n".format(payload))
        lora.println(payload)

        counter += 1
        sleep(.25)

class TermRead:
    """
    We create  a select.poll() object called spoll, and register the standard input (sys.stdin) with the POLLIN
    flag, indicating that we want to wait for the standard input to be ready for reading.

    When we call spoll.poll(0), the 0 parameter specifies a milliseconds timeout value of 0, 
    which means that the poll() method will return immediately with a list of file descriptors that
    have events to process, or an empty list if no events are ready to be processed.

    This allows us to check if there's input available on sys.stdin without waiting for any input to arrive.
    """
    def __init__(self):
        self.spoll = select.poll()
        self.spoll.register(sys.stdin, select.POLLIN)
        
    
    def read(self):
        txt = ''
        while self.spoll.poll(0):
            # see the other versions here for utf-8 characters
            txt += sys.stdin.read(1)
        return txt


if __name__ == '__main__':
    
    spi = SPI(0, baudrate=5000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))

    freq = 433E6
    
    lora = SX127x(spi=spi,
              pins={'ss' : Pin(17, Pin.OUT),
                    'reset':Pin(14, Pin.OUT),
                    'dio_0':Pin(15, Pin.IN)},
              parameters = {
            'frequency': freq, 
            'tx_power_level': 2, 
            'signal_bandwidth': 125E3,    
            'spreading_factor': 8, 
            'coding_rate': 5, 
            'preamble_length': 8,
            'implicit_header': False, 
            'sync_word': 0x12, 
            'enable_CRC': False,
            'invert_IQ': False,
            })
    
    term = TermRead()
    while True:
        text = term.read()
        if text != '':
            send(lora,text)
        receive(lora)
