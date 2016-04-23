import serial
import time
import utils
import Process

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
        time.sleep(2)
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
        response = ''
        self.modem.write('AT+CMGF=1\r')
        time.sleep(1)
        self.modem.write('AT+CNMI=2,1,0,0,0\r\n');
        time.sleep(1)
        #self.modem.write('AT+CMGL="ALL"r\r');
        while True:
            out = self.modem.readline();
            print(out)
            if "+CMTI" in out:
                utils.getMessage(self.modem, utils.getMessageIndex(out))
            elif "REC UNREAD" in out:
            #else:
                body = self.modem.readline()
                while(not process.process.authorized):
                    try:
                        process.process.authorize(body.split(' ')[0], body.split(' ')[1])
                    except:
                        response = "Please send your username and password, split by a whitespace"

                if (process.process.authorized):
                    response = process.execute(body.splitlines()[0])

                time.sleep(1)


                # self.modem.write('AT+CMGF=0\r')
                # time.sleep(1)

                # print('response:' + response[0:])
                # dpu = '0011000C914861555195810000FF05F4F29C1E03'
                # dpu = '0041000C91486155519581000003050003000201986F79'

                # print('sending')
                # strS = 'AT+CMGS=' + str(len(dpu) / 2 - 1) + '\r';
                # print(strS)
                # self.modem.write(strS)
                # time.sleep(1)
                # self.modem.write(dpu);
                # time.sleep(1)
                # self.modem.write(chr(26))
                # time.sleep(1)

                # self.modem.write('AT+CMGF=0\r')
                # time.sleep(1)
                # print('done')

                # dpu = '0041000C91486155519581000001050003000202FF0131'
                # dpu = '0041000C91486155519581000003050003000202986F79'

                # self.modem.write('AT+CMGS=' + str(len(dpu) / 2 - 1) + '\r')
                # time.sleep(1)
                # self.modem.write(dpu);
                # time.sleep(1)
                # self.modem.write(chr(26))
                # time.sleep(1)
                # print('done 2')


                count = 0
                while True:
                    utils.send(self.modem, vuBinh, response[count:count + 159])
                    count += 160
                    if (count > len(response)):
                        break

                # clear mem
                self.modem.write('AT+CMGD=1,2\r\n')
                time.sleep(2)
