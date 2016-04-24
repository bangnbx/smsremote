import paramiko

class RemoteProcess():
    def __init__(self, username, password, hostname):
        self.cwd = ""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname, username = username, password = password)
        except:
            print "Sorry, we can't SSH to your server. Please try again  later."

    def execute(self, command):
        args = command.split(" ")
        dirChanged = False
        currentDir = ""
        if (args[0] == "cd"):
            dirChanged = True
            currentDir = args[1]

        command = "cd " + self.cwd + "&& " + command
        # handle incorrect commands
        try:
            stdin, stdout, stderr = self.client.exec_command(command);
            if stdout.channel.recv_exit_status() == 0:
                output = stdout.read()
            else:
                output = stderr.read()
        except:
            output = "Error when connect to server"

        # change directory if necessary
        if (dirChanged):
            stdin, stdout, stderr = self.client.exec_command('pwd');
            self.cwd = stdout.read().rstrip() + "/" + currentDir
            output = self.cwd
        return output
