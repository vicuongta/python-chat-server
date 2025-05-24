import socket
import sys
import select
import os
import termios

USERNAME = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])
NUM_MSG = int(sys.argv[4]) if len(sys.argv) > 4 else 50 # number of latest messages, retrieve 50 newest messages if not passed in

# create an INET, STREAMing socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

chat_history = []

# Parse chat history from a string into a list of dictionaries
def handleChatHistory(data):
    lines = data.strip().split('\n')
    for line in lines[1:]:
        if ': ' in line:
            username, message = line.split(': ', 1)
            chat_history.append({'username': username, 'message': message.strip()})
        else:
            chat_history.append({'username': line.strip(':'), 'message': ''})
    # return chat_history[-NUM_MSG:]

# Reprint chat history
def loadChat(chat, num):
    print(f'LOGGED IN AS {USERNAME}\n')
    newest_message = chat[-num:]
    for message in newest_message:
        print(f"{message['username']}: {message['message']}")
    print(f'>> {user_input}', end='', flush=True)

fd = sys.stdin.fileno()
original_attr = termios.tcgetattr(fd)

try:
    # Set the terminal to non-canonical input mode
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON
    newattr[3] = newattr[3] & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    user_input = ''

    while True:
        readable, writable, exceptional = select.select([sys.stdin, client_socket], [], [sys.stdin, client_socket])
        for source in readable:
            # print existing messages received from server
            if source is client_socket:
                data = client_socket.recv(1024).decode()
                if data:
                    chat_history = []
                    handleChatHistory(data)
                    print('\033[2J\033[H', end='')
                    loadChat(chat_history, NUM_MSG)
                else:
                    client_socket.close()
                    print('Server Disconnected')
                    sys.exit(0)
            elif source is sys.stdin:
                char = sys.stdin.read(1)
                # ESC or Ctrl+C is pressed
                if char == '\x1b' or char == '\x03':
                    client_socket.close()
                elif char == '\n': # User pressed Enter
                    message = f'{USERNAME}: {user_input}'
                    client_socket.send(message.encode())
                    print(f'Message sent: {user_input}')
                    user_input = ''
                elif char == '\x7f': # User press Backspace
                    user_input = user_input[:-1]
                    print('\b \b', end='', flush=True)
                else:
                    user_input += char
                    print(char, end='', flush=True)

except KeyboardInterrupt:
    print("\nReceived KeyboardInterrupt, exiting...")
except Exception as e:
    print('Error:', e)
finally:
    termios.tcsetattr(fd, termios.TCSANOW, original_attr)
    client_socket.close()
    print('Server disconnected!')