import time
import serial

def send(modem, number, message):
    modem.write('ATZ\r')
    time.sleep(1)
    modem.write('AT+CMGF=1\r')
    time.sleep(1)
    modem.write('''AT+CMGS="''' + number + '''"\r''')
    time.sleep(1)
    modem.write(message + "\r")
    time.sleep(1)
    modem.write(chr(26))
    time.sleep(1)

def getMessageIndex(indicator):
    index = indicator.strip().split(',')[1]
    return index

def getMessage(modem, index):
    modem.write('AT+CMGR=' + index + '\r')
