def chat():
    with open('chat_history_stats.txt', 'r') as file:
        lines = file.readlines()
        buffer = []
        for line in lines[-100:]:
            buffer.append(line)
        return buffer

chat_buffer = chat()
print(chat_buffer)