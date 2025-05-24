import socket
import sys
import time

USERNAME = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])
NUM_MSG = int(sys.argv[4]) if len(sys.argv) > 4 else 50  # number of latest messages, retrieve 50 newest messages if not passed in
BUFFER_SIZE = 8192

# create an INET, STREAMing socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# chat_history = []
message_sent = 0
message_recv = 0

# Parse chat history from a string into a list of dictionaries
# def handleChatHistory(data):
#     lines = data.strip().split('\n')
#     for line in lines:
#         if ': ' in line:
#             username, message = line.split(': ', 1)
#             chat_history.append({'username': username, 'message': message.strip()})
#         else:
#             chat_history.append({'username': line.strip(':'), 'message': ''})

# # Reprint chat history
# def loadChat(chat, num):
#     newest_message = chat[-num:]
#     for message in newest_message:
#         print(f"{message['username']}: {message['message']}")

try:
    print('Sending messages as fast as possible...')
    while True:
        data = client_socket.recv(BUFFER_SIZE).decode()
        if data:
            message_recv += 1
            if data == 'quit':
                print(f'Server sent {data}!')
                break
            else:
                # handleChatHistory(data)
                # print('\033[H\033[J', end='') # Refresh screen by deleting old chat
                # loadChat(chat_history, NUM_MSG)
                message = f'{USERNAME}: Pew!\n'
                client_socket.send(message.encode())
                message_sent += 1
        else:
            client_socket.close()
            sys.exit(0)

except KeyboardInterrupt:
    print("\nReceived KeyboardInterrupt, exiting...")
except Exception as e:
    print('Error:', e)
finally:
    print('Server Disconnected!')
    print(f"{USERNAME} sent {message_sent} messages and received {message_recv} messages!")  # Print the number of messages sent
    total_messsages = message_sent + message_recv
    print(f'{USERNAME} processessed {total_messsages} messages!')
    client_socket.close()
    sys.exit(message_sent)  # Exit with the number of messages sent