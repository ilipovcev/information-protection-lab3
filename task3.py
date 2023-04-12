#  Задание № 3
#
# Алгоритм шифрования rsa.
#
# Сгенерируйте открытый и закрытый ключи в алгоритме шифрования RSA, выбрав простые числа p = 271 и q = 227.
# Зашифруйте сообщение: Факт - самая упрямая в мире вещь.
import math
import random


def is_prime(n):
    """Проверка числа на простоту"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_prime_number():
    """Генерация случайного простого числа"""
    prime = False
    while not prime:
        p = random.randint(100, 500)
        if is_prime(p):
            return p


p = 271
q = 227

n = p * q
phi = (p - 1) * (q - 1)

# Выбираем случайное число e, которое является взаимно простым с phi
while True:
    e = random.randint(2, phi - 1)
    if math.gcd(e, phi) == 1:
        break

# Вычисляем число d, обратное к e по модулю phi
d = pow(e, -1, phi)

public_key = (n, e)
private_key = (n, d)

print("Открытый ключ:", public_key)
print("Закрытый ключ:", private_key)

message = "Факт - самая упрямая в мире вещь."
message_bytes = message.encode("utf-8")

# Преобразуем сообщение в число
message_int = int.from_bytes(message_bytes, byteorder="big")

# Разбиваем сообщение на блоки, чтобы зашифровать каждый отдельно
block_size = math.floor(math.log2(n) / 8)
blocks = [message_int >> i * block_size & 2 ** block_size - 1 for i in
          range(math.ceil(message_int.bit_length() / block_size))]

# Шифруем каждый блок отдельно
encrypted_blocks = [pow(block, e, n) for block in blocks]

# Объединяем зашифрованные блоки в одно число
encrypted = sum(encrypted_block << i * block_size for i, encrypted_block in enumerate(encrypted_blocks))

print("Зашифрованное сообщение:", hex(encrypted))

# Разбиваем зашифрованное число на блоки, чтобы расшифровать каждый отдельно
decrypted_blocks = [pow(encrypted >> i * block_size & 2 ** block_size - 1, d, n) for i in range(len(blocks))]

# Объединяем расшифрованные блоки в одно число
decrypted = sum(decrypted_block << i * block_size for i, decrypted_block in enumerate(decrypted_blocks))

# Преобразуем число обратно в байтовую строку
decrypted_bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, byteorder="big")

# Декодируем байтовую строку в исходную строку
decrypted_message = decrypted_bytes.decode("utf-8")

print("Расшифрованное сообщение:", decrypted_message)

