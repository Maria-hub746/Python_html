import socket
import json


def run_client(ip, port, message: dict):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    data = json.dumps(message).encode()
    sock.sendto(data, server)
    print(f'Send data: {data.decode()} to server: {server}')
    response, address = sock.recvfrom(1024)
    print(f'Response data: {response.decode()} from address: {address}')
    sock.close()
    return int(response.decode())