from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
from threading import Thread
import client
import udp_server

HOST = 'localhost'
PORT = 3000


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index_homework.html')
        elif pr_url.path == '/message':
            self.send_html_file('mesage.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data: bytes = self.rfile.read(int(self.headers['Content-Length']))
        data_parse: str = urllib.parse.unquote_plus(data.decode())
        data_dict: dict = urllib.parse.parse_qs(data_parse)
        code = client.run_client(HOST, PORT, data_dict)
        self.send_response(code)
        if code == 302:
            self.send_header('Location', '/')
        else:
            self.send_header('Location', '/error.html')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    path_data = pathlib.Path.joinpath(pathlib.Path().absolute(), 'storage')
    if not path_data.exists():
        pathlib.Path.mkdir(path_data)
        path_data = pathlib.Path.joinpath(path_data, 'data.json')
        path_data.touch(exist_ok=True)
        path_data.write_text('{}')
    server_address = ('', 5000)
    http = server_class(server_address, handler_class)
    try:
        server = Thread(target=udp_server.udp_server, args=(HOST, PORT))
        server.start()
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
