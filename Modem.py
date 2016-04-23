import serial 
import time
import utils
import Process

vuBinh = "+841655155918"
dungChuot = "+841697448948"

class Modem():
    modem = ""
    def __init__(self):
        port = "/dev/ttyUSB2"
        baudrate = 115200
        self.modem = serial.Serial(port, baudrate, timeout = 5, bytesize = serial.EIGHTBITS)
        if self.modem.isOpen():
            print ("port " + self.modem.name + ' is open...')
        self.modem.write('AT+CMGD=1,2\r\n')
        time.sleep(2)



    def test(self):
        while True:
            cmd = raw_input("Enter command or 'exit':")
            if cmd == 'exit':
                self.modem.close()
                exit()
            elif cmd == 'unread':
                self.modem.write('AT+CMGL="REC UNREAD"\r')
            elif 'send' in cmd:
                message = cmd.split(':')[1]
                utils.send(self.modem, vuBinh, message)
            elif cmd == 'listen':
                self.modem.write('AT+CNMI=2,1,0,0,0\r');
                while True:
                    out = self.modem.readline();
                    #print(out)    
                    if "+CMTI" in out:
                        utils.getMessage(self.modem, utils.getMessageIndex(out))
                    elif "REC UNREAD" in out:
                        body = self.modem.readline()
                        print(body)
            else:
                print "wrong cmd"

    def run(self):
        process = Process.Process()
        self.modem.write('AT+CMGF=1\r')
        time.sleep(1)
        self.modem.write('AT+CNMI=2,1,0,0,0\r\n');
        time.sleep(2)
        self.modem.write('AT+CMGL="ALL"r\r');
        while True:
            out = self.modem.readline();
            print(out)    
            if "+CMTI" in out:
                utils.getMessage(self.modem, utils.getMessageIndex(out))
            elif "REC UNREAD" in out:
                body = self.modem.readline()
                print('body:' + body.splitlines()[0] + ':endbody')
                response = process.execute(body.splitlines()[0])
                print('response:' + response)
                time.sleep(1)
                utils.send(self.modem, vuBinh, response)
                # clear mem
                self.modem.write('AT+CMGD=1,2\r\n')
                time.sleep(2)


       