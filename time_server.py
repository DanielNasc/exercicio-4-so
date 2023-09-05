import socket
import threading
import datetime
from sys import stderr

HOST: str = 'localhost'  # Standard loopback interface address (127.0.0.1)
PORT: int = 8082  # Port to listen on (non-privieged ports are > 1023)
DATA_PAYLOAD: int = 1024  # The maximum amount of data to be received at once

routines = {
    'd': lambda: datetime.datetime.now().date(),
    't': lambda: datetime.datetime.now().time(),
    'dt': lambda: datetime.datetime.today(),
}

def str_adrr(address) -> str:
    return f'\033[31m{address[0]}:{address[1]}\033[m'

def receive(client, address) -> None:

    
    print('Waiting to receive a message from client...', file=stderr)
    data = client.recv(DATA_PAYLOAD)
    message = data.decode()

    if message:
        print('Received message from client', str_adrr(address), file=stderr)

        if message in routines:
            message = routines[message]()
        else:
            client.sendall('400'.encode())
            print('Closing client connection', str_adrr(address), file=stderr)
            client.close()
            return

        message = str(message)

        client.sendall(message.encode())
    else:
        client.sendall('400'.encode())

    print('Closing client connection', str_adrr(address), file=stderr)
    client.close()


# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
SERVER_ADDRESS = (HOST, PORT)
print('\033[34m''Starting up echo server on %s port %s''\033[m' %
      SERVER_ADDRESS)

sock.bind(SERVER_ADDRESS)

MAX_QUEUE_CONNECT: int = 7  # specifies the max no, of queued connections
sock.listen(MAX_QUEUE_CONNECT)  # Listen to clients

while True:
    client, address = sock.accept()
    connection = threading.Thread(target=receive,args=(client, address))
    connection.start()