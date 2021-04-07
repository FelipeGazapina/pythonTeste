import socket
import selectors
import types

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr= addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data= data)
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

sel = selectors.DefaultSelector()

HOST = '127.0.0.1' # endereço localhost
PORT = 65432 # porta que roda o servidor
# socket.socket cria um objeto socket que suporta context manager type, então pode-se usar um with para não ser necessário fechar a comunicação
# o que é passado no socket() especifica o endereço familiar e o type do socket
# AF_INET é o endereço familiar da internet para IPV4
# SOCK_STREAM é o typo de socket para o protocolo TCP que vai ser usado para transmitir as mensagens
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()

print('listenting on', (HOST, PORT))

lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data= None)

while True: # loop infinito é usado para ler as chamadas que vem do cliente com conn.recv()
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
