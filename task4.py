# Задание № 4
#
# Функция хеширования.
#
# Найти хеш–образ своей Фамилии, используя хеш–функцию MD5.

import struct
from enum import Enum
from math import (
    floor,
    sin,
)

from bitarray import bitarray


class MD5Buffer(Enum):
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476


class MD5(object):
    _string = None
    _buffers = {
        MD5Buffer.A: None,
        MD5Buffer.B: None,
        MD5Buffer.C: None,
        MD5Buffer.D: None,
    }

    @classmethod
    def hash(cls, string):
        cls._string = string

        preprocessed_bit_array = cls._step_2(cls._step_1())
        cls._step_3()
        cls._step_4(preprocessed_bit_array)
        return cls._step_5()

    @classmethod
    def _step_1(cls):
        # Преобразование строки в битовый массив.
        bit_array = bitarray(endian="big")
        bit_array.frombytes(cls._string.encode("utf-8"))

        # Добавление к строке 1 бита и столько нулевых битов, чтобы длина
        # битового массива стала сравнимой с 448 по модулю 512.
        # Обратите внимание, что дополнение всегда выполняется, даже если
        # длина битового массива уже сравнима с 448 по модулю 512, что
        # приводит к новому блоку сообщения длиной 512 бит.
        bit_array.append(1)
        while len(bit_array) % 512 != 448:
            bit_array.append(0)

        # Для оставшейся части алгоритма MD5 все значения находятся
        # в формате little endian, поэтому преобразуем битовый массив
        # в little endian.
        return bitarray(bit_array, endian="little")

    @classmethod
    def _step_2(cls, step_1_result):
        # Расширяем результат из шага 1 64-битным числом, представленным в little-endian
        # и соответствующим остатку от деления длины исходного сообщения на 2^64.
        length = (len(cls._string) * 8) % pow(2, 64)
        length_bit_array = bitarray(endian="little")
        length_bit_array.frombytes(struct.pack("<Q", length))

        result = step_1_result.copy()
        result.extend(length_bit_array)
        return result

    @classmethod
    def _step_3(cls):
        # Инициализируем буферы значениями по умолчанию.
        for buffer_type in cls._buffers.keys():
            cls._buffers[buffer_type] = buffer_type.value

    @classmethod
    def _step_4(cls, step_2_result):
        # Определяем четыре вспомогательные функции, которые производят одно 32-битное слово.
        F = lambda x, y, z: (x & y) | (~x & z)
        G = lambda x, y, z: (x & z) | (y & ~z)
        H = lambda x, y, z: x ^ y ^ z
        I = lambda x, y, z: y ^ (x | ~z)

        # Определяем функцию циклического сдвига влево на `n` бит.
        rotate_left = lambda x, n: (x << n) | (x >> (32 - n))

        # Определяем функцию модулярного сложения.
        modular_add = lambda a, b: (a + b) % pow(2, 32)

        # Вычисляем таблицу T из функции синуса. Обратите внимание, что
        # RFC начинается с индекса 1, но мы начинаем с индекса 0.
        T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]

        # Общее количество 32-битных слов для обработки, N, всегда кратно 16.
        N = len(step_2_result) // 32

        # Обрабатываем блоки по 512 бит.
        for chunk_index in range(N // 16):
            # Разбиваем блок на 16 слов по 32 бит в списке X.
            start = chunk_index * 512
            X = [step_2_result[start + (x * 32): start + (x * 32) + 32] for x in range(16)]

            # Преобразуем объекты `bitarray` в целые числа.
            X = [int.from_bytes(word.tobytes(), byteorder="little") for word in X]

            # Создаем краткие ссылки на буферы A, B, C и D.
            A = cls._buffers[MD5Buffer.A]
            B = cls._buffers[MD5Buffer.B]
            C = cls._buffers[MD5Buffer.C]
            D = cls._buffers[MD5Buffer.D]

            # Выполняем четыре раунда по 16 операций в каждом.
            for i in range(4 * 16):
                if 0 <= i <= 15:
                    k = i
                    s = [7, 12, 17, 22]
                    temp = F(B, C, D)
                elif 16 <= i <= 31:
                    k = ((5 * i) + 1) % 16
                    s = [5, 9, 14, 20]
                    temp = G(B, C, D)
                elif 32 <= i <= 47:
                    k = ((3 * i) + 5) % 16
                    s = [4, 11, 16, 23]
                    temp = H(B, C, D)
                elif 48 <= i <= 63:
                    k = (7 * i) % 16
                    s = [6, 10, 15, 21]
                    temp = I(B, C, D)

                temp = modular_add(temp, X[k])
                temp = modular_add(temp, T[i])
                temp = modular_add(temp, A)
                temp = rotate_left(temp, s[i % 4])
                temp = modular_add(temp, B)

                # Swap the registers for the next operation.
                A = D
                D = C
                C = B
                B = temp

            # Update the buffers with the results from this chunk.
            cls._buffers[MD5Buffer.A] = modular_add(cls._buffers[MD5Buffer.A], A)
            cls._buffers[MD5Buffer.B] = modular_add(cls._buffers[MD5Buffer.B], B)
            cls._buffers[MD5Buffer.C] = modular_add(cls._buffers[MD5Buffer.C], C)
            cls._buffers[MD5Buffer.D] = modular_add(cls._buffers[MD5Buffer.D], D)

    @classmethod
    def _step_5(cls):
        A = struct.unpack("<I", struct.pack(">I", cls._buffers[MD5Buffer.A]))[0]
        B = struct.unpack("<I", struct.pack(">I", cls._buffers[MD5Buffer.B]))[0]
        C = struct.unpack("<I", struct.pack(">I", cls._buffers[MD5Buffer.C]))[0]
        D = struct.unpack("<I", struct.pack(">I", cls._buffers[MD5Buffer.D]))[0]

        return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"


message = 'Липовцев'
print('message: ' + message)
print('md5 hash: ' + MD5.hash(message))
