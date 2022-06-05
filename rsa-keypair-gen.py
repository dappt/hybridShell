from Cryptodome.PublicKey import RSA

new_key = RSA.generate(4096) # generate  RSA key that 4096 bits long

#Export the Key in PEM format, the PEM extension contains ASCII encoding
publicKey = new_key.publickey().exportKey("PEM")
privateKey = new_key.export_key("PEM")
publicKey_file = open("public.pem", "wb")
publicKey_file.write(public_key)
publicKey_file.close()
privateKey_file = open("private.pem", "wb")
privateKey_file.write(private_key)
privateKey_file.close()

print(publicKey.decode())
print(privateKey.decode())