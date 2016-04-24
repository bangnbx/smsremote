import SubProcessor
import os
import Modem

class Process():
    def __init__(self):
        self.process = SubProcessor.SubProcessor(os.getcwd())
        #self.process.authorized = True

    def login(self, username, passwd):
        result = process.authorize(username, passwd)
        print result

    def execute(self, command):
        response = self.process.run(command)
        return response

    def getUserInfo(self, username):
        try:
            return self.process.users[username]
        except:
            return "User isn't login"

    def main(self):
        while (not process.authorized):
            getUserInfo()
        command = ''
        response = ''

        modem = Modem.Modem()
        modem.run(process)

        while(command != 'exit'):
            # command = raw_input("$ ")

            response = process.run(command)
            print response
