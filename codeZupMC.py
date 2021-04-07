import random
import time as tempo
import socket
import keyboard

ClientSocket = socket.socket()
host = socket.gethostname()
port = 12333

chat = ''
countdown: float = 0
increment: int = 1
randInt = int(random.randrange(3, 6))

print('Waiting for connection')
def format(bWord):
    return str(bWord).replace('b', '').replace("'", '')
def parImpar(number):
    if number%2 == 0:
        return "Number Par"
    return "Number Ímpar"

def incrementFunc(client,plus_plus):
    global randInt
    global countdown
    global increment
    tempo.sleep(0.5)
    countdown = countdown + 0.5
    print("Math: ", increment, "+", plus_plus)
    increment = increment + plus_plus
    print("Countdown: ", countdown, "Until this number -> ", randInt)
    if randInt <= countdown:
        client.send(str('render').encode('utf-8'))
        plus_plus = int(format(client.recv(1024)))
        print("Random Number Received: ", plus_plus, " ", parImpar(plus_plus))
        countdown = 0
        randInt = random.randrange(3, 6)
        client.send(str(increment).encode('utf-8'))
        return int(plus_plus)
    else:
        client.send(str(increment).encode('utf-8'))
        return int(plus_plus)



try:
    ClientSocket.connect((host, port))
except socket.error as err:
    print(str(err))

Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
Input = input('Login: ')
ClientSocket.send((str.encode(Input)))
plus_plus = format(ClientSocket.recv(1024))
while True:
    if keyboard.is_pressed('esc'):
        break
    try:
        plus_plus = int(str(plus_plus))
        plus_plus = incrementFunc(ClientSocket, plus_plus)
    except ValueError:
        chat = increment
        increment = 1



    # função 0.5s chamar servidor para enviar increment



ClientSocket.close()