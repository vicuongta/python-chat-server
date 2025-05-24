import sys
import socket
import select
import os
import time

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8822
FILE_PATH = 'chat_history.txt'
BUFFER_SIZE = 8192
CHAT_HISTORY_BUFFER_SIZE = 50
TOTAL_TIME = 30

# Create a server socket to listen to incoming messages
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Non-blocking, so that select can deal with the multiplexing
server_socket.setblocking(False)

# Bind the socket to a public host, and a well-known port
hostname = socket.gethostname()
server_socket.bind(('', PORT))
server_socket.listen(200)
print(f'Listening on interface {hostname}:{PORT}')

clients = []
chat_history_buffer = []

# Statistics
message_sent = 0
message_recv = 0

def loadChatHistory(path):
    with open(path, 'r') as file:
        chat = file.read()
        return chat

def writeToChat(path, message):
    with open(path, 'a') as file:
        file.write(message + '\n')

def broadcastMessage(message, receiver):
    count = 0
    for r in receiver:
        r.send(message.encode())
        count += 1
    return count

def writeToBuffer(message):
    chat_history_buffer.append(message)

def addConnection(source):
    clients.append(source)

def removeConnection(source):
    if source in clients:
        clients.remove(source)
    if source in inputs:
        inputs.remove(source)
    source.close()

def createFile(path):
    with open(path, 'w') as file:
        file.write('Welcome to Discordn\'t. Start chatting here\n\n')
    print('Chat History Stats Created! Ready for test!')

def deleteAndRecreateFile(path):
    if os.path.exists(path):
        os.remove(path)
    createFile(path)

try:
    # Check file existence and create
    if not os.path.exists(FILE_PATH):
        createFile(FILE_PATH)
    else:
        deleteAndRecreateFile(FILE_PATH)
        
    # Start timer
    start_time = time.time()

    while True:
        print('Waiting for input...')
        print(f'Message received: {message_recv}')
        inputs = [server_socket] + clients
        readable, writable, exceptional = select.select(inputs, [], inputs)
        for source in readable:
            if source is server_socket:
                client_socket, client_addr = server_socket.accept()
                print(f'New connection at {client_addr}')
                addConnection(client_socket)

                chat_history = loadChatHistory(FILE_PATH)
                if chat_history:
                    client_socket.send(chat_history.encode())
                else:
                    print('Error loading chat history! Exiting')
                    removeConnection(client_socket)
            else:
                data = source.recv(BUFFER_SIZE).decode()
                if data:
                    messages = data.split('\n') # separate messages when received at the same time
                    for m in range(len(messages)-1):
                        writeToChat(FILE_PATH, messages[m])
                        message_recv += 1 # increment count for each message received and written to history
                        message_sent += broadcastMessage(messages[m], clients)                                    
                else:
                    print(f'Client {source.getpeername()} disconnected.')
                    removeConnection(source)

        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time >= TOTAL_TIME:
            break

        # Write any remaining chat history to the file
        if chat_history_buffer:
            for message in chat_history_buffer:
                writeToChat(FILE_PATH, message)
            chat_history_buffer = []

except KeyboardInterrupt:
    print("\nReceived KeyboardInterrupt, exiting...")
except Exception as e:
    print('Error:', e)
finally:
    print(f'In {round(elapsed_time/60, 4)} minutes:')
    print(f'The server receives {message_recv} messages and sent {message_sent} messages!')
    total_messages = message_recv + message_sent
    print(f'The server processed {total_messages} messages!')
    broadcastMessage('quit', clients)
    # Remove all connections
    clients = []
    print('Closing socket! Exiting!')
    server_socket.close()
    inputs = []
    sys.exit(0)