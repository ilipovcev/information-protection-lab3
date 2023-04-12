# Задание № 5
#
# Электронная цифровая подпись.
#
# Используя хеш-образ строки: << Да, он прав, тысячу раз прав этот дуб, думал князь Андрей.>>
# И вычислите электронную цифровую подпись по схеме RSA.

import hashlib
import random


# Определяем функцию для получения хеш-образа строки
def md5_hash(message):
    md5 = hashlib.md5()
    md5.update(message.encode('utf-8'))
    return int(md5.hexdigest(), 16)


# Генерируем ключи RSA
def generate_rsa_keys():
    # Выбираем два случайных простых числа p и q
    p = generate_prime_number()
    q = generate_prime_number()
    # Вычисляем модуль n и функцию Эйлера phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    # Выбираем случайное целое число e, взаимно простое с phi(n)
    e = random.randint(2, phi_n - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)
    # Вычисляем закрытую экспоненту d
    d = modular_inverse(e, phi_n)
    return (e, n), (d, n)


# Определяем функцию для нахождения наибольшего общего делителя
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Определяем функцию для нахождения обратного элемента в кольце по модулю
def modular_inverse(a, m):
    # Расширенный алгоритм Евклида
    old_r, r = a, m
    old_s, s = 1, 0
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    # Если old_r == 1, то обратный элемент существует
    if old_r == 1:
        return old_s % m
    else:
        raise ValueError("modular inverse does not exist")


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


message = "Да, он прав, тысячу раз прав этот дуб, думал князь Андрей."

# Вычисляем хеш-образ строки
hash_message = md5_hash(message)
print("Хеш-образ строки:", hash_message)

# Генерируем ключи RSA
public_key, private_key = generate_rsa_keys()
hash_value = md5_hash(message)
signature = pow(hash_value, private_key[0], private_key[1])

print('Цифровая подпись: ' + str(signature))

print('public_key: ' + str(public_key))
print('private_key: ' + str(private_key))
