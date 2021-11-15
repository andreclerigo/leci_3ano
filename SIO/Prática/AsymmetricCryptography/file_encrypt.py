import sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


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

    key_size = (public_key.key_size + 7)//8
    cyphertext = []

    with open (input_file, "rb") as input_file:
        while (message := input_file.read(key_size - 66)):
            cyphertext.append(public_key.encrypt(
                            message,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        ))
    
    with open (output_file, "wb") as output_file:
        for c in cyphertext:
            output_file.write(c)

if __name__ == '__main__':
    main()
    