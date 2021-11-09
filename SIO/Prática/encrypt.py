import sys
import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


ALGORITHMS = [ "AES-128", "ChaCha20" ]

def main():
    salt = os.urandom(16)

    if len(sys.argv) < 4:
        print("Error - Insufficient number of arguments")
        exit(1)

    file_name = sys.argv[1]
    file_destination = sys.argv[2]
    algorithm_name = sys.argv[3]   

    if algorithm_name not in ALGORITHMS:
        print("Error - Invalid algorithm specified")        
        exit(1)
    
    password = input("Insert the password to transform into a key: ")
    
    key = generate_key(password, algorithm_name, salt)
    generate_file(file_name, file_destination, key, algorithm_name)

    with open('salt.txt', 'wb') as file:
        file.write(salt)

def generate_file(file_name, file_destination, key, algorithm):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    with open(file_name, "rb") as file:
        data = file.read()

    if algorithm == "AES-128":
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        a = "AES-128"
    elif algorithm == "ChaCha20":
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        a = "ChaCha20"

    with open(file_destination, "wb") as file:
        file.write(iv)
        file.write(encrypted_data)

    with open('algorithm.txt', 'w') as file:
        file.write(a)

def generate_key(password, algorithm, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )

    key = kdf.derive(password.encode())
    
    if algorithm == "AES-128":
        key = key[:16]
    elif algorithm == "ChaCha20":
        key = key[:64]

    return key


if __name__ == "__main__":
    main()
