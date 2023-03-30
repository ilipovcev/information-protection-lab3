from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
file_out.close()

file_in = open("receiver.pem", "rb")
public_key = RSA.import_key(file_in.read())

cipher_rsa = PKCS1_OAEP.new(public_key)
message = "Факт - самая упрямая в мире вещь."
message_bytes = message.encode('utf-8')

encrypted = cipher_rsa.encrypt(message_bytes)
print(encrypted)

private_key = RSA.import_key(open("private.pem").read())
# создаем объект шифра PKCS1_OAEP с использованием приватного ключа
cipher_rsa = PKCS1_OAEP.new(private_key)
# расшифровываем сообщение
decrypted = cipher_rsa.decrypt(encrypted)

message = decrypted.decode('utf-8')
print(message)



