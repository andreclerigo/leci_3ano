import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def main():
    size = int(input("Enter the size of the key: "))

    if size not in [1024, 2048, 4096]:
        print("Invalid key size must be 1024 or 2048 or 4096!")
        sys.exit(1)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=size,
    )

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    pem_public = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_name = input("Enter the name of the private key file: ")
    public_name = input("Enter the name of the public key file: ")

    with open(private_name, "wb") as f:
        f.write(pem_private)
    
    with open(public_name, "wb") as f:
        f.write(pem_public)


if __name__ == '__main__':
    main()
