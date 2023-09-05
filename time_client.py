import socket
from sys import argv

#HOST: str = '10.0.84.179'
HOST: str = 'localhost'
PORT: int = 8082

FLAGS: list[str] = ['d', 't', 'dt']

class InputExcept(Exception):
    message = 'Invalid input flags!\nUsage: python3 time_client.py [-d | -t | -dt]'

    def __init__(self):
        super().__init__(self.message)

# Se comunica com o servidor e recebe a resposta
def get(sock: socket.socket, code: str) -> str:
    sock.sendall(code.encode())

    DATA_PAYLOAD: int = 1024
    data = sock.recv(DATA_PAYLOAD)

    return data.decode()

# Pega a entrada do usuário, seja por argumento ou por input
def get_input(args) -> str:
    filtred_args = filter_input(args) # Filtra os argumentos passados pelo usuário

    if filtred_args != '':  # Se o usuário passou um argumento
        return filtred_args

    print('Choose an option:')
    options = ['0 - exit:', '1 - date:', '2 - time:', '3 - datetime:']
    for option in options:
        print(option)

    message = input('>>> ') # Pega a entrada do usuário
    try:
        message = int(message) # Tenta converter a entrada para inteiro
        flag = FLAGS[message] # Pega a flag correspondente ao número digitado
        return flag
    except (ValueError, IndexError): # Se não for um inteiro ou não existir a flag correspondente
        raise InputExcept

# (args = -d | -t | -dt)
def filter_input(args: list) -> str:
    if len(args) == 0:
        return ''

    if len(args) > 1:
        raise InputExcept
    
    flag = args[0][1:]

    if flag in FLAGS:
        return flag
    
    raise InputExcept

def main(*args) -> None:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    CLIENT_ADDRESS = (HOST, PORT)
    print('Connection to %s port %s' % CLIENT_ADDRESS)

    # Connect the socket to the server
    sock.connect(CLIENT_ADDRESS)

    try:
        message = get_input(args)
        # Send/ Receive data
        print(f'Received: {get(sock, message)}')
    except InputExcept as e:
        print(e)

    print('Closing connection to the server')
    sock.close()


if __name__ == '__main__':
    main(*argv[1:])