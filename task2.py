#  Задание № 2
#
# Алгоритм шифрования DES.
#
# Зашифруйте строку: <<Да, человек смертен, но это было бы еще полбеды.>>
# Алгоритмом DES в режиме сцепления блоков.

from Cryptodome.Util.Padding import pad
from Cryptodome.Cipher import DES

# устанавливаем ключ шифрования
key = b"secretaa"

# задаем исходную строку для шифрования
message = "Да, человек смертен, но это было бы еще полбеды."

# создаем объект DES с режимом CBC
cipher = DES.new(key, DES.MODE_CBC)

# разбиваем строку на блоки размером 64 бита и шифруем каждый блок
encrypted_blocks = []
for i in range(0, len(message), 8):
    block = message[i:i+8].encode('utf-8')
    padded_block = pad(block, 8)
    encrypted_block = cipher.encrypt(padded_block)
    encrypted_blocks.append(encrypted_block)

# объединяем зашифрованные блоки в зашифрованную строку
encrypted_message = b"".join(encrypted_blocks)

# выводим зашифрованную строку в шестнадцатеричном виде
print("Зашифрованная строка: ", encrypted_message.hex())
