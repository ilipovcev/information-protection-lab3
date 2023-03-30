from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import hashlib

# генерируем пару ключей
key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)
file_out.close()
public_key = key.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
file_out.close()

# создаем объект хеш-функции MD5 и получаем хеш-образ сообщения
message = "Да, он прав, тысячу раз прав этот дуб, думал князь Андрей."
message_hash = hashlib.md5(message.encode()).hexdigest()

# создаем объект шифра PKCS1_OAEP с использованием закрытого ключа и шифруем хеш-образ
private_key = RSA.import_key(open("private.pem").read())
cipher_rsa = PKCS1_OAEP.new(private_key)
message_hash_bytes = message_hash.encode('utf-8')
signature = cipher_rsa.encrypt(message_hash_bytes)

print(signature.hex())  # выводим электронную цифровую подпись в шестнадцатеричном виде
