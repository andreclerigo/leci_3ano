import sys
import os
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def main():
    # Check if the user has provided the correct number of arguments
    if len(sys.argv) < 2:
        print("Usage: python3 encrypt.py <input_file> <output_file>")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read the bytes from the input file
    with open(input_file, "rb") as file:
        data = file.read()
    
    password = input("Insert the password to transform into a key: ")
    
    # Encrypt the data
    encrypted_data, nonce, salt, signature = encrypt(data, password)

    # Write the encrypted data to the output file with nonce, salt, signature and cryptogram
    with open(output_file, "wb") as file:
        file.write(nonce)
        file.write(salt)
        file.write(signature)
        file.write(encrypted_data)

def encrypt(data, password):
    salt = os.urandom(32)
    nonce = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )

    # Derive the key from the password
    key = kdf.derive(password.encode())

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    
    # Create the signature
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(encrypted_data)
    signature = h.finalize()

    return encrypted_data, nonce, salt, signature

if __name__ == "__main__":
    main()
