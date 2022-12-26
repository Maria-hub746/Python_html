from datetime import datetime
import json
import socket
import pathlib


def udp_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = host, port
    sock.bind(server)
    try:
        while True:
            data_byte, address = sock.recvfrom(1024)
            data = json.loads(data_byte.decode())
            print(f'Received data: {data} from: {address}')
            try:
                path = pathlib.Path('storage/data.json')
                json_data = json.loads(path.read_text(encoding='utf-8'))
                json_data[str(datetime.now())] = {'username': data['username'][0], 'message': data['message'][0]}
                path.write_text(json.dumps(json_data, ensure_ascii=False, indent=4), encoding='utf-8')
                sock.sendto(b'302', address)
                print(f'Send data: {data} to: {address}')
            except Exception as e:
                sock.sendto(b'404', address)

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()