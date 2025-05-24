I put codes for each part in individual directory (part_1 and part_2) so there's no confusion.
Part 1: 
1) How to start the server:
Run 'python3 server.py' to start the server, the server is by default running on port 8822 and it will print the interface it's listening on. If you want to change to another port, run 'python3 server.py $PORT' where $PORT is your desired PORT.
The server would block and wait for connection from the client(s).
2) How to start client:
The client.py accepts 4 arguments, USERNAME, HOST, PORT, and an optional NUM_MSG to show number of messages (by default will be 20 messages).
Here I put a sample run command I would use: 'python3 client.py tavc heron.cs.umanitoba.ca 8822 50' where heron.cs.umanitoba and 8822 are the HOST and PORT printed by the server. You can omit the last argument since I put by default 20 messages to show.
You can connect 2 clients to check for the incoming messages.
