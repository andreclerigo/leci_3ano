import sys
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def main():
    # Check if the user has provided the correct number of arguments
    if len(sys.argv) < 2:
        print("Usage: python3 decrypt.py <input_file> <output_file>")
        exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read the bytes from the input file
    # Associate the right parameters to nonce, salt and signature
    with open(input_file, 'rb') as input_file:
        nonce = input_file.read(16)
        salt = input_file.read(32)
        signature = input_file.read(32)
        data = input_file.read()
    
    password = input("Insert the password to transform into a key: ")

    # Decrypt the data
    decrypted_data = decrypt(data, password, nonce, salt, signature)

    # Write the decrypted data to the output file
    with open(output_file, 'wb') as output_file:
        output_file.write(decrypted_data)

def decrypt(data, password, nonce, salt, signature):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )

    # Derive the key from the password
    key = kdf.derive(password.encode())

    # Verify the signature before decrypting (error is thrown if the signature is not valid)
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    h.verify(signature)

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()

    return decrypted_data


if __name__ == '__main__':
    main()
