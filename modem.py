import serial 
import time

vuBinh = "+841655155918"
dungChuot = "+841697448948"

readPort = "/dev/ttyUSB2"
writePort = "/dev/ttyUSB2"
baud = 9600
baud = 115200


writeSer = serial.Serial(writePort, baud, timeout = 5, bytesize = serial.EIGHTBITS)
readSer = serial.Serial(readPort, baud, timeout = 5, bytesize = serial.EIGHTBITS)


def send(number, message):
    writeSer.write('ATZ\r')
    time.sleep(1)
    writeSer.write('AT+CMGF=1\r')
    time.sleep(1)
    writeSer.write('''AT+CMGS="''' + number + '''"\r''')
    time.sleep(1)
    writeSer.write(message + "\r")
    time.sleep(1)
    writeSer.write(chr(26))
    time.sleep(1)
    out = ""
    while readSer.inWaiting() > 0:
        out += readSer.read()
    out += "=============\n"
    out += readSer.read(128)
    print('Receiving...' + out)

def getMessageIndex(indicator):
    index = indicator.strip().split(',')[1]
    return index

def getMessage(modem, index):
    modem.write('AT+CMGR=' + index + '\r')


if writeSer.isOpen():
    print ("write port " + writeSer.name + ' is open...')

if readSer.isOpen():
    print ("read port " + readSer.name + ' is open...')

while True:
    
    cmd = raw_input("Enter command or 'exit':")
    if cmd == 'exit':
        writeSer.close()
        readSer.close()
        exit()
    elif cmd == 'unread':
        #writeSer.write(cmd.encode('ascii')+'\r')
        print cmd
        # check inbox
        writeSer.write('AT+CMGL="REC UNREAD"\r')
        time.sleep(3)
        out = ""
        while readSer.inWaiting() > 0:
            out += readSer.read()
        out += "=============\n"
        out += readSer.read(128)
        print('Receiving...' + out)
 
        
        #writeSer.write('AT+CMGD=1,2')
    elif cmd == 'send':
        send(vuBinh, "haah")
    elif cmd == 'listen':
        writeSer.write('AT+CNMI=2,1,0,0,0\r');
        while True:
            out = readSer.readline();
            # print('-----')
            # print(out)    
            # print('-----')        
            if "+CMTI" in out:
                getMessage(writeSer, getMessageIndex(out))
            elif "REC UNREAD" in out:
                body = readSer.readline()
                print(body)
    else:
        print "wrong cmd"



