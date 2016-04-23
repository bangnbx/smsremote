import SubProcessor
import os

process = SubProcessor.SubProcessor(os.getcwd())

def login(username, passwd):
    result = process.authorize(username, passwd)
    print result

def execute(command):
    response = process.run(command)
    return response

def getUserInfo():
    username = ''
    passwd = ''
    while (username == ''):
        username = raw_input("Your username: ")
    while(passwd == ''):
        passwd = raw_input("Your password: ")
    login(username, passwd)

def main():
    while (not process.authorized):
        getUserInfo()
    command = ''
    response = ''
    while(command != 'exit'):
        command = raw_input("$ ")
        response = process.run(command)
        print response

main()
