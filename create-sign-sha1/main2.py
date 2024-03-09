from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import utils

import time

def create_cms_signer(p12_file_path, passphrase):
    # Load .p12 file
    with open(p12_file_path, 'rb') as p12_file:
        p12_data = p12_file.read()

    # Load .p12 data
    p12 = pkcs12.load_pkcs12(p12_data, passphrase.encode(), default_backend())

    # Get private key and certificate from .p12
    private_key = p12.key
    certificate = p12.cert.certificate

    # Create CMS signer
    signer = (
        x509.CertificateSigningRequestBuilder(
            subject_name=certificate.subject,
        )
        .add_attribute(
            x509.SignatureAlgorithmOID.RSA_WITH_SHA1,
            b'\x05\x00',  # Signature Algorithm Parameters
            # x509.ATTR_NO_VALUE
        )
        .add_attribute(
            x509.ExtensionOID.SIGNED_CERTIFICATE_TIMESTAMPS,
            str(time.time()).encode(),
            # x509.ATTR_NO_VALUE
        )
        .sign(private_key, hashes.SHA256(), default_backend())
    )
    return signer

# Example usage
p12_file_path = './CA_b10.p12'
passphrase = ''  # Set your passphrase

cms_signer = create_cms_signer(p12_file_path, passphrase)
print('==>', cms_signer.public_bytes(encoding=serialization.Encoding.PEM))