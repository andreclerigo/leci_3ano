import sys
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from decrypt import decrypt


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 decrypt_hybrid.py <input_file> <output_file> <key_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    key_file = sys.argv[3]

    with open (key_file, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    key_size = (private_key.key_size + 7)//8
    # print(key_size)

    with open (input_file, "rb") as input_file:
        key = input_file.read(key_size)
        iv = input_file.read(16)
        data = input_file.read()

    decrypted_key = private_key.decrypt(
                        key,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )

    decrypted_data = decrypt(data, decrypted_key, "AES-128", iv)

    with open(output_file, "wb") as output_file:
        output_file.write(decrypted_data)

if __name__ == '__main__':
    main()
    