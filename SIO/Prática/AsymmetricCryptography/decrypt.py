import sys
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from encrypt import generate_key


ALGORITHMS = [ "AES-128", "ChaCha20" ]

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 decrypt.py <input_file> <output_file> <algorith_name>")
        exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    algorithm_name = sys.argv[3]   

    if algorithm_name not in ALGORITHMS:
        print("Error - Invalid algorithm specified")        
        exit(1)

    with open(input_file, 'rb') as input_file:
        iv = input_file.read(16)
        salt = input_file.read(16)
        data = input_file.read()

    password = input("Insert the password to transform into a key: ")
    key = generate_key(password, algorithm_name, salt)

    decrypted_data = decrypt(data, key, algorithm_name, iv)
    unpadded_data = unpadder(decrypted_data, algorithm_name)

    with open(output_file, 'wb') as output_file:
        output_file.write(unpadded_data)

def unpadder(decrypted_data, algorithm_name):
    padder = padding.PKCS7(128).padder()
    
    if algorithm_name == "AES-128":
        return padder.update(decrypted_data) + padder.finalize()
    elif algorithm_name == "ChaCha20":
        return decrypted_data

def decrypt(data, key, algorithm_name, iv):    
    if algorithm_name == "AES-128":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    elif algorithm_name == "ChaCha20":
        cipher = Cipher(algorithms.ChaCha20(key, iv), mode=None)

    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()
    return decrypted_data


if __name__ == '__main__':
    main()
