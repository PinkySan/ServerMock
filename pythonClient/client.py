import argparse
import logging
import socket
import struct
import sys
import threading
from datetime import datetime, timezone

__version__ = '1.0.0'

# TCP message format constants (to be updated according to tcpmessage.prompt.md)
STARTBIT = 0xAA
HEADER_FORMAT = '>BHB'  # Example: startbit (1 byte), length (2 bytes), msg_id (1 byte)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
CHECKSUM_SIZE = 1  # 1 byte checksum

# Example message IDs (to be updated as needed)
KNOWN_MESSAGE_IDS = {1: 'Ping', 2: 'Pong'}


def utc_now_str():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f UTC')


def calc_checksum(data: bytes) -> int:
    """Simple checksum: sum of all bytes modulo 256."""
    return sum(data) % 256


def build_message(msg_id: int, payload: bytes) -> bytes:
    length = HEADER_SIZE + len(payload) + CHECKSUM_SIZE
    header = struct.pack(HEADER_FORMAT, STARTBIT, length, msg_id)
    msg = header + payload
    checksum = calc_checksum(msg) & 0xFF
    return msg + bytes([checksum])


def parse_message(data: bytes):
    if len(data) < HEADER_SIZE + CHECKSUM_SIZE:
        raise ValueError('Message too short')
    startbit, length, msg_id = struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])
    if startbit != STARTBIT:
        raise ValueError('Invalid startbit')
    if length != len(data):
        raise ValueError('Invalid length')
    payload = data[HEADER_SIZE:-CHECKSUM_SIZE]
    checksum = data[-1]
    if calc_checksum(data[:-1]) != checksum:
        raise ValueError('Invalid checksum')
    return msg_id, payload


def log_message(direction, msg_id, payload):
    msg_name = KNOWN_MESSAGE_IDS.get(msg_id, f'Unknown({msg_id})')
    logging.info(f"{utc_now_str()} {direction} [ID={msg_id} {msg_name}] Payload: {payload.hex()}")


def receive_loop(sock):
    try:
        while True:
            # Read header first
            header = sock.recv(HEADER_SIZE)
            if not header:
                logging.error('Server closed connection')
                break
            try:
                startbit, length, msg_id = struct.unpack(HEADER_FORMAT, header)
            except Exception as e:
                logging.error(f'Invalid header: {e}')
                continue
            # Read rest of message
            rest = b''
            to_read = length - HEADER_SIZE
            while to_read > 0:
                chunk = sock.recv(to_read)
                if not chunk:
                    logging.error('Server closed connection')
                    return
                rest += chunk
                to_read -= len(chunk)
            data = header + rest
            try:
                msg_id, payload = parse_message(data)
                log_message('RECV', msg_id, payload)
            except Exception as e:
                logging.error(f'Invalid message: {e}')
    except Exception as e:
        logging.error(f'Receive error: {e}')


def main():
    parser = argparse.ArgumentParser(description='TCP Client for Rust Server')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=2345, help='Server port (default: 12345)')
    parser.add_argument('--msg-id', type=int, help='Message ID to send')
    parser.add_argument('--payload', type=str, help='Hex payload to send (e.g. "010203")')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    try:
        sock = socket.create_connection((args.host, args.port), timeout=5)
    except Exception as e:
        logging.error(f'Could not connect to server: {e}')
        sys.exit(1)

    logging.info(f'Connected to {args.host}:{args.port}')

    recv_thread = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
    recv_thread.start()

    ## Send the message with id 1 and the payload 0xAABBCCDD at start
    payload = 0x08154217.to_bytes(4, byteorder='big')  # Example payload
    msg = build_message(1, payload)
    # Add 4-byte big-endian length prefix for Rust server compatibility
    msg_with_len = len(msg).to_bytes(4, byteorder='big') + msg
    sock.sendall(msg_with_len)
    log_message('SEND', 1, payload)


    if args.msg_id is not None:
        try:
            payload = bytes.fromhex(args.payload) if args.payload else b''
            msg = build_message(args.msg_id, payload)
            # Add 4-byte big-endian length prefix for Rust server compatibility
            msg_with_len = len(msg).to_bytes(4, byteorder='big') + msg
            sock.sendall(msg_with_len)
            log_message('SEND', args.msg_id, payload)
        except Exception as e:
            logging.error(f'Failed to send message: {e}')
    else:
        logging.info('No message sent. Use --msg-id and --payload to send a message.')

    try:
        recv_thread.join()
    except KeyboardInterrupt:
        logging.info('Exiting...')
    finally:
        sock.close()

if __name__ == '__main__':
    main()
