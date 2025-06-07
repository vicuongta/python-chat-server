# 💬 Python Chat Server - Discordn't

A simple terminal-based chat server and client system that mimics the basic functionality of a messaging platform, built using Python sockets.

## 🚀 Features

- Full-duplex chat between two terminal clients.
- TCP and UDP socket communication support.
- Message encryption via serialization and deserialization.
- Message logging system to retrieve conversation history.
- Performance test mode using Bash script for stress simulation.

## 📂 Repository Structure

```
├── server.py          # Server that handles incoming client connections
├── client.py          # Client for sending/receiving messages
├── udp_version/       # Modified UDP implementation for testing
│   ├── udp_server.py
│   └── udp_client.py
├── test_script.sh     # Bash script to spawn multiple clients and simulate chat load
└── README.md
```

## 🧪 Performance Simulation

A test mode using UDP was created to:
- Simulate real-time message exchange between multiple clients.
- Run for a duration of 5 minutes.
- Collect statistics on send/receive cycles and message stability.

## 🛠 How to Run

### Server
```bash
python3 server.py
```

### Client
```bash
python3 client.py [SERVER_IP] [PORT]
```

### UDP Test Mode
```bash
bash test_script.sh
```

## 🧠 Concepts Used

- Python socket programming (TCP/UDP)
- Serialization using `pickle`
- Bash scripting for automation
- Multithreading for full-duplex communication

## 📄 License

This project is licensed under the MIT License.