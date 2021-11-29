import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def main():
    if (len(sys.argv) < 2):
        print("Usage: validity_interval.py <certificate>")
        sys.exit(1)

    cert_file = sys.argv[1]
    with open(cert_file, 'rb') as cert_file:
        cert_data = cert_file.read()

    cert = x509.load_pem_x509_certificate(cert_data, default_backend())

    if valid_cert(cert):
        print("Certificate is valid")
    else:
        print("Certificate is not valid")


def valid_cert(cert):
    if cert.not_valid_before < cert.not_valid_after:
        return True
    else:
        return False

if __name__ == '__main__':
    main()
    