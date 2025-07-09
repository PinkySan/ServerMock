---
mode: edit
description: Configurable Rust server 
---
# TCP Server

* Create a Rust server that can be configured by the user with arguments
* By default, the server should listen on `127.0.0.1:2345`
* The server should be able to send TCP messages to clients
* The server must only support a single client at a time
* The server must receive a tcp message from the client and respond with a message
* The server must implement the TCP message format specified in the `tcpmessage.prompt.md` file


# Logging
* The server must log all received messages and sent messages with the current UTC time
* The server must log the client address and port of the connected client