---
mode: agent
description: Client for testing the Rust server
---

# TCP Client
* Create a client with python that can connect to the Rust server
* The client should be able to send TCP messages to the server
* The client must implement the TCP message format specified in the `tcpmessage.prompt.md` file
* The client must also receive messages from the server and print them to the console
* The client should be able to handle multiple message IDs
* Must print the received messages to the console with the current UTC time
* Must print the sent messages to the console with the current UTC time
* The client should be able to send a message with a specific message ID and payload
* The client must be configurable by the user with command line arguments
* The client must use the `argparse` library for command line argument parsing
* The client must be able to handle errors gracefully and print error messages to the console
* The client must be able to handle the case where the server is not reachable
* The client must be able to handle the case where the server is not responding
* The client must be able to handle the case where the server sends an invalid message
* The client must be able to handle the case where the server sends a message with an unknown message ID
* The client must be able to handle the case where the server sends a message with an invalid payload
* The client must be able to handle the case where the server sends a message with an invalid header
* The client must be able to handle the case where the server sends a message with an invalid checksum
* The client must be able to handle the case where the server sends a message with an invalid startbit
* The client must be able to handle the case where the server sends a message with an invalid length
* The client must be able to handle the case where the server sends a message with an invalid message ID
* The client must be able to handle the case where the server sends a message with an invalid payload length
* The client must be able to handle the case where the server sends a message with an invalid header length
* The client must be able to handle the case where the server sends a message with an invalid checksum length
* The client must be able to handle the case where the server sends a message with an invalid startbit length
* The client must be able to handle the case where the server sends a message with an invalid message ID length
* The files must be placed in a ${workspaceFolder}/pythonClient
* A python environment must be created with `python -m venv .venv`
* The client must be able to run with `python -m pythonClient.client`
* The client must be able to run with `python -m pythonClient.client --help` to show the help message
* The client must be able to run with `python -m pythonClient.client --version`
* The client must be able to run with `python -m pythonClient.client --host <host> --port <port>` to specify the host and port
* The client must use a 3rd party library for TCP communication, such as `socket`
* The client must use a 3rd party library for logging, such as `logging`