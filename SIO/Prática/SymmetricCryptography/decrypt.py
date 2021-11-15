import sys
import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from encrypt import generate_key


def main():
    if len(sys.argv) < 2:
        exit(1)
    
    file_name = sys.argv[1]

    with open('algorithm.txt', 'r') as file:
        a = file.read()


    with open(file_name, 'rb') as file:
        if a == "ChaCha20":
            salt = file.read(16)
            file.seek(16)
        else:
            file.seek(16)
            salt = file.read(16)
            file.seek(32)

        data = file.read()

    password = input("Insert the password to transform into a key: ")
    key = generate_key(password, a, salt)

    decrypted_data = decrypt(key, data, a)
    unpadded_data = unpadder(decrypted_data, a)

    with open('decifrado', 'wb') as file:
        file.write(unpadded_data)

def unpadder(decrypted_data, a):
    padder = padding.PKCS7(128).padder()
    
    if a == "AES-128":
        return padder.update(decrypted_data) + padder.finalize()
    elif a == "ChaCha20":
        return decrypted_data

def decrypt(key, data, a):
    with open('cifrado', 'rb') as file:
        iv = file.read(16)
    
    if a == "AES-128":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    elif a == "ChaCha20":
        cipher = Cipher(algorithms.ChaCha20(key), modes.ChaCha20Poly1305(iv))

    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(data) + decryptor.finalize()
    return decrypted_data


if __name__ == '__main__':
    main()
