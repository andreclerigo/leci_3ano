import sys
import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.modes import ECB


ALGORITHMS = [ "AES-128", "ChaCha20" ]

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 encrypt.py <input_file> <output_file> <algorithm_name>")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    algorithm_name = sys.argv[3]   

    if algorithm_name not in ALGORITHMS:
        print("Error - Invalid algorithm specified")        
        exit(1)

    salt = os.urandom(16)
    iv = os.urandom(16)
    
    password = input("Insert the password to transform into a key: ")
    key = generate_key(password, algorithm_name, salt)

    with open(input_file, "rb") as file:
        data = file.read()
    
    encrypted_data = encrypt(data, key, algorithm_name, iv)
    with open(output_file, "wb") as file:
        file.write(iv)
        file.write(salt)
        file.write(encrypted_data)

def encrypt(data, key, algorithm, iv):
    if algorithm == "AES-128":
        cipher = Cipher(algorithms.AES(key), modes.ECB())
    elif algorithm == "ChaCha20":
        cipher = Cipher(algorithms.ChaCha20(key, iv), mode=None)

    encryptor = cipher.encryptor()
    
    if algorithm == "AES-128":
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    elif algorithm == "ChaCha20":
        encrypted_data = encryptor.update(data) + encryptor.finalize()
    
    return encrypted_data

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
