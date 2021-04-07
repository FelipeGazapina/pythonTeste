import socket
import random
from _thread import *


ServerSocket = socket.socket()
host = socket.gethostname()
port = 12333
ThreadCount = 0

try:
    ServerSocket.bind((host, port))
except socket.error as err:
    print(str(err))

print('Waiting for a connection')
ServerSocket.listen()

def format(bWord):
    return str(bWord).replace('b', '').replace("'", '')


def saveUserData(user, data):
    file = open("usersBD/" + str(user) + '.txt', 'w')
    file.write(str(user + ' ' + str(data) + '\n'))
    file.close()


def userNumbersCheck(user): #save <user> <value>
    file = open(("usersBD/" + str(user) + '.txt'), 'r')
    for line in file:
        value = line.split()
        return value[1]

def saveComunication(user, comunication):
    file = open('log.txt', 'a+')
    file.write('User: ' + str(user) + ' - Comunication: ' + str(comunication) + '\n')
    file.close()


def verifyUser(user, users=None):
    file = open('users.txt', 'r')
    read = file.readlines()
    for line in read:
        if str(user) in line:
            return True
    return False
def createUser(user):
    file = open('users.txt', 'a+')
    file.write(str(user) + '\n')
    file.close()
    saveUserData(user, '1')

def comunication(connection, user):
    while True:
        data = format(connection.recv(2048))
        if not data:
            connection.send(str.encode('Closing connection...'))
            saveComunication(user, 'Closing...')
            break
        if data == 'render':
            rand = str(random.randrange(0, 99))
            print("Random Number: ", rand, " of ", user)
            connection.send(rand.encode('utf-8'))
            saveUserData(user, rand)
        else:
            saveComunication(user, data)

def threaded_client(connection):
    connection.send(str.encode('Welcome! Who are you? ESC to Exit'))
    user = format(connection.recv(2048))
    saveComunication(user, 'Starting...')
    print('Start comunication and verify user')
    if verifyUser(user) == True:
        print('Checking increment of user')
        print("Starting User -> ", user)
        increment = userNumbersCheck(user)
        if increment == None:
            connection.send(str(1))
        else:
            connection.send(str(increment).encode('utf-8'))
            comunication(connection, user)
    else:
        createUser(user)
        saveComunication(user, "Creating...")
        print("Creating User -> ", user)
        increment = 1
        connection.send(str(increment).encode('utf-8'))
        comunication(connection, user)
    connection.close()


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number : ' + str(ThreadCount))
ServerSocket.close()