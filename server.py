import sys
import socket
import select
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8822
FILE_PATH = 'chat_history.txt'

# Create a server socket to listen to incoming messages
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Non-blocking, so that select can deal with the multiplexing
server_socket.setblocking(False)

# Bind the socket to a public host, and a well-known port
hostname = socket.gethostname()
server_socket.bind(('', PORT)) # connect
server_socket.listen(5)
print(f'Listening on interface {hostname}:{PORT}')

clients = []
inputs = [server_socket] + clients

def loadChatHistory(path):
    with open(path, 'r') as file:
        chat = file.read()
        return chat

def writeToChat(path, message):
    with open(path, 'a') as file:
        file.write(message + '\n')

def broadcastMessage(message, receiver):
    for r in receiver:
        try:
            r.send(message.encode())
            print(f'Server sent message: {message}')
        except:
            removeConnection(r)

def addConnection(source):
    clients.append(source)
    inputs.append(source)

def removeConnection(source):
    if source in clients:
        clients.remove(source)
    if source in inputs:
        inputs.remove(source)
    source.close()

try:
    # Check file existence and create
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as file:
            file.write('Welcome to Discordn\'t. Start chatting here\n\n')
        print('Chat History Created!')

    while True:
        print('Waiting for input...')
        readable, writable, exceptional = select.select(inputs, [], inputs)
        for source in readable:
            if source is server_socket: # new client
                client_socket, client_addr = server_socket.accept()
                print(f'New connection at {client_addr}')
                addConnection(client_socket)

                chat_history = loadChatHistory(FILE_PATH)
                if chat_history:
                    client_socket.send(chat_history.encode())
                else:
                    welcome_message = 'Welcome to Discordn\'t'
                    writeToChat(FILE_PATH, welcome_message)
            else:
                data = source.recv(1024).decode()
                # print(f'data: {data}')
                if data:
                    message = data.split(': ', 1)[1].strip()
                    print(f'Message received: {message}')
                    writeToChat(FILE_PATH, data)
                    broadcastMessage(data, clients)
                else:
                    print(f'Client {source.getpeername()} disconnected.')
                    removeConnection(source)
        for source in exceptional:
            print(f'Handling exception for {source.getpeername()}')
            removeConnection(source)

except KeyboardInterrupt:
    print("\nReceived KeyboardInterrupt, exiting...")
except Exception as e:
    print('Error:', e)
finally:
    server_socket.close()
    print('Closing socket! Exiting!')
    sys.exit(0) # successful termination