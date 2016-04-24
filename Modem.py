import serial
import time
import utils
import Process
import RemoteProcess

vuBinh = "+841655155918"
dungChuot = "+841697448948"
ngoc = "+84962202323"
SMSC = "+84980200030"

class Modem():
    modem = ""
    def __init__(self):
        port = "/dev/ttyUSB2"
        baudrate = 115200
        self.modem = serial.Serial(port, baudrate, timeout = 5, bytesize = serial.EIGHTBITS)
        if self.modem.isOpen():
            print ("port " + self.modem.name + ' is open...')
        self.modem.write('AT&F\r\n')
        time.sleep(1)
        self.modem.write('AT+CMGD=1,2\r\n')
        time.sleep(0.5)

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
        response = ''
        authorized = False
        username = ""
        password = ""
        self.modem.write('AT+CMGF=1\r')
        time.sleep(1)
        self.modem.write('AT+CNMI=2,1,0,0,0\r\n');
        time.sleep(1)
        #self.modem.write('AT+CMGL="ALL"r\r');
        while True:
            out = self.modem.readline();
            if (out != ''):
                print(out)
            if "+CMTI" in out:
                utils.getMessage(self.modem, utils.getMessageIndex(out))
            elif "REC UNREAD" in out:
            #else:
                body = self.modem.readline()

                if (not authorized):
                    try:
                        username = body.split(' ')[0]
                        password = body.split(' ')[1]
                        response = process.process.authorize(username, password)
                    except:
                        response = "Please send your username and password, split by a whitespace"
                    if (process.process.authorized):
                        authorized = True                        
                else:
                    host = process.getUserInfo(username)[1]
                    if host != '127.0.0.1':
                        process = RemoteProcess.RemoteProcess('root', 'v@(qbU7Cx7T7', "112.78.3.74")
                    response = process.execute(body.splitlines()[0])
                    if (response==''):
                        response = body.splitlines()[0] + " was successfully called"

                utils.sendLongMessage(self.modem, ngoc, response)
                # count = 0
                # while True:
                #     count += 160
                #     if (count > len(response)):
                #         break

                # clear mem
                self.modem.write('AT+CMGD=1,2\r\n')
                time.sleep(0.5)
