import PyKCS11
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


lib = '/usr/local/lib/libpteidpkcs11.so'
pkcs11 = PyKCS11.PyKCS11Lib()
pkcs11.load(lib)
slots = pkcs11.getSlotList()

for slot in slots:
    print(pkcs11.getTokenInfo(slot))

    all_attr = list(PyKCS11.CKA.keys())
    #Filter attributes
    all_attr = [e for e in all_attr if isinstance(e, int)]

    session = pkcs11.openSession(slot)
    for obj in session.findObjects():
        # Get object attributes
        attr = session.getAttributeValue(obj, all_attr)
        # Create dictionary with attributes
        attr = dict(zip(map(PyKCS11.CKA.get, all_attr), attr))

        print('Label: ', attr['CKA_LABEL'])        
        print('\tType: ', attr['CKA_CLASS'])
        print('\tID: ', attr['CKA_ID'])

        if attr['CKA_CLASS'] == PyKCS11.CKO_CERTIFICATE:
            if attr['CKA_ID'][0] == 70:     # signature
                cert = x509.load_der_x509_certificate( bytes(attr['CKA_VALUE']), default_backend())

        if attr['CKA_CLASS'] == PyKCS11.CKO_PRIVATE_KEY:
            if attr['CKA_ID'][0] == 70:     # signature
                private_key = obj


text = b'Ola o meu nome e Andre Clerigo'
mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
signature = bytes(session.sign(private_key, text, mechanism))
with open('sign.bin', 'wb') as f:
    f.write(signature)

public_key = cert.public_key()
public_key.verify(signature, text, padding.PKCS1v15(), hashes.SHA1())
