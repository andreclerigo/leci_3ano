import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hashes import MD5, SHA256, SHA384, SHA512


HASH_FUNCTIONS = ['MD5', 'SHA256', 'SHA384', 'SHA512']

def main():
    if len(sys.argv) != 4:
        print("Usage: hash_file.py <input_file> <output_file> <hash_function>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    hash_function = sys.argv[3]

    if hash_function not in HASH_FUNCTIONS:
        print("Invalid hash function")
        sys.exit(1)

    with open(input_file, 'rb') as f:
        data = f.read()
    
    hashed_data = hash_data(data, hash_function)

    with open(output_file + '_' + hash_function, 'wb') as f:
        f.write(hashed_data)

    
def hash_data(data, hash_function):
    if hash_function == 'MD5':
        digest = hashes.Hash(hashes.MD5())
    if hash_function == 'SHA256':
        digest = hashes.Hash(hashes.SHA256())
    if hash_function == 'SHA384':
        digest = hashes.Hash(hashes.SHA384())
    if hash_function == 'SHA512':
        digest = hashes.Hash(hashes.SHA512())

    digest.update(data)
    hashed_data = digest.finalize()

    return hashed_data

    
if __name__ == '__main__':
    main()
    