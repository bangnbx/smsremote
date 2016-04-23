import serial 
import time
import utils

vuBinh = "+841655155918"
dungChuot = "+841697448948"

port = "/dev/ttyUSB2"
baudrate = 115200

modem = serial.Serial(port, baudrate, timeout = 5, bytesize = serial.EIGHTBITS)

if modem.isOpen():
    print ("port " + modem.name + ' is open...')

while True:
    cmd = raw_input("Enter command or 'exit':")
    if cmd == 'exit':
        modem.close()
        exit()
    elif cmd == 'unread':
        modem.write('AT+CMGL="REC UNREAD"\r')
    elif 'send' in cmd:
        message = cmd.split(':')[1]
        utils.send(modem, vuBinh, message)
    elif cmd == 'listen':
        modem.write('AT+CNMI=2,1,0,0,0\r');
        while True:
            out = modem.readline();
            #print(out)    
            if "+CMTI" in out:
                utils.getMessage(modem, utils.getMessageIndex(out))
            elif "REC UNREAD" in out:
                body = modem.readline()
                print(body)
    else:
        print "wrong cmd"

def run():
    modem.write('AT+CNMI=2,1,0,0,0\r');
    while True:
        out = modem.readline();
        #print(out)    
        if "+CMTI" in out:
            utils.getMessage(modem, utils.getMessageIndex(out))
        elif "REC UNREAD" in out:
            body = modem.readline()
            print(body)

