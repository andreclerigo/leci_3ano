from validity_interval import valid_cert
import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend


certs_dict = {}

def main():
    all_files = os.scandir("/etc/ssl/certs")
    for f in all_files:
        if f.is_file():
            load_cert(f)

    print(certs_dict)

def load_cert(path):
    try:
        with open(path, "rb") as reader:
            cert_data = reader.read()

        cert = x509.load_pem_x509_certificate(cert_data, default_backend())

        if valid_cert(cert):
            certs_dict[cert.subject.rfc4514_string()] = cert
            
    except Exception as e:
        print("Error: ", e, "\n")

if __name__ == '__main__':
    main()
    