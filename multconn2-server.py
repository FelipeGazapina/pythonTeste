import socket
import _thread

def on_new_client(clientsocket, addr):
    while True:
        msg = clientsocket.recv(1024)
        print(addr, '>>>', msg)
        msg = raw_input('SERVER>>')
        clientsocket.send(msg)
    clientsocket.close()


s = socket.socket()
host = socket.gethostname()
port = 50000

print('Server Started and are waiting for clients...')

s.bind((host,port))
s.listen(5)

print('Got connection from ')
while True:
    c,addr = s.accept()
    _thread.start_new_thread(on_new_client(c,addr))
s.close()