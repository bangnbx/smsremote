import time
import serial

def send(modem, number, message):
    # modem.write('ATZ\r')
    # time.sleep(1)
    modem.write('AT+CMGF=1\r')
    time.sleep(0.5)
    modem.write('''AT+CMGS="''' + number + '''"\r''')
    time.sleep(0.5)
    modem.write(message + "\r")
    time.sleep(0.5)
    modem.write(chr(26))
    time.sleep(0.5)
    modem.write('AT+CNMI=2,1,0,0,0\r\n');
    time.sleep(0.5)

def getMessageIndex(indicator):
    index = indicator.strip().split(',')[1]
    return index

def getMessage(modem, index):
    modem.write('AT+CMGR=' + index + '\r\n')
    time.sleep(0.5)
