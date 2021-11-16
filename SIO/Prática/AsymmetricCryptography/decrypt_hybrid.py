import sys
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from encrypt import encrypt


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 file_encrypt.py <input_file> <output_file> <key_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    key_file = sys.argv[3]

    with open (key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )

    with open (input_file, "rb") as input_file:
        data = input_file.read()

    salt = os.urandom(16)
    iv = os.urandom(16)
    password = input("Insert the password to transform into a key: ")
    key = generate_key(password, salt)
    
    key_encrypted = public_key.encrypt(
                        key,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )

    encrypted_data = encrypt(data, key_encrypted[:16], "AES-128", iv)

    with open (output_file, "wb") as output_file:
        output_file.write(key_encrypted)
        output_file.write(iv)
        output_file.write(encrypted_data)

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )

    key = kdf.derive(password.encode())

    return key[:16]

if __name__ == '__main__':
    main()
    