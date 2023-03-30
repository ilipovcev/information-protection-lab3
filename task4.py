import hashlib

surname = "Липовцев"

# преобразование строки в байты
surname_bytes = surname.encode('utf-8')

# хеширование байтовой строки
hash_object = hashlib.md5(surname_bytes)

# получение хеш-значения в виде строки
hash_hex = hash_object.hexdigest()

# вывод результата
print("Хеш-образ фамилии:", hash_hex)
