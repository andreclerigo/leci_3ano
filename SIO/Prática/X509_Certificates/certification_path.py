from trust_anchors import load_cert
import sys
import os


certs_dict = {}

def main():
    all_files = os.scandir("/etc/ssl/certs")
    for f in all_files:
        if f.is_file():
            load_cert(f)

    for cert in certs_dict:
        chain = get_issuers(cert)
        print(chain)

def get_issuers(certificate, chain=[]):
    # print(certificate)
    # print('ISSUER ' + str(certs_dict[certificate].issuer))
    chain.append(certificate)

    issuer = certs_dict[certificate].issuer
    subject = certs_dict[certificate].subject

    if issuer == subject and subject in certs_dict:
        print("Chain complete")
        return chain
    
    if issuer in certs_dict:
        return get_issuers(certs_dict[issuer], certs_dict, chain)

    print("Unable to create the Trust Chain")
    return chain


if __name__ == '__main__':
    main()
    