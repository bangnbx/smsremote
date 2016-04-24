import subprocess
import os
import mysql.connector
import paramiko

DB_CONFIG = {
  'user': 'root',
  'password': '1',
  'host': '127.0.0.1',
  'database': 'sms_db',
  'raise_on_warnings': True,
}


class SubProcessor():

    def __init__(self, cwd):
        self.cwd = cwd
        self.users = {}
        try:
            cnx = mysql.connector.connect(**DB_CONFIG)
            cursor = cnx.cursor(buffered=True)
            query = "SELECT username, passwd, hostname FROM users"
            cursor.execute(query)
            for (u, p, h) in cursor:
                self.users[u] = (p, h)
            cursor.close()
            cnx.close()
        except IOError:
            print "IOError"
        self.authorized = False

    def authorize(self, user, password):
        correct_pw = ""
        try:
            password = password.strip()
            user = user.strip()
            correct_pw = self.users[user][0]

            if correct_pw == password:
                self.authorized = True
                return "Authorization success."
            else:
                return "Authorization failed. Try again."
        except KeyError:
            return "Authorization failed. Try again."


    def run(self, command):
        if (not self.authorized):
            return "Server access not authorized."
        # change directory to current (as defined by previously executed commands)
        os.chdir(self.cwd)

        # handle directory changes
        command = command[0].lower() + command[1:]
        args = command.split(" ")
        dirChanged = False
        if (args[0] == "cd"):
            #command += "; pwd"
            dirChanged = True

        # handle incorrect commands
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True);
        except subprocess.CalledProcessError as e:
            output = e.output.replace(":", "")
            dirChanged = False

        # change directory if necessary
        if (dirChanged):
            self.cwd = subprocess.check_output(command+"; pwd", shell=True).strip()
            output = self.cwd
        return output
