# Python TCP Client for Rust Server

This package provides a command-line TCP client for testing the Rust server.

## Features
- Connects to the Rust server via TCP
- Sends and receives messages using the specified TCP message format
- Handles multiple message IDs and error cases
- Configurable via command line arguments
- Logs all sent and received messages with UTC timestamps

## Usage

1. Create a virtual environment:

    python -m venv .venv

2. Activate the virtual environment:

    - On Windows:
        .venv\Scripts\activate
    - On Unix or MacOS:
        source .venv/bin/activate

3. Install dependencies:

    pip install -r requirements.txt

4. Run the client:

    python -m pythonClient.client --host <host> --port <port>

5. Show help:

    python -m pythonClient.client --help

6. Show version:

    python -m pythonClient.client --version
