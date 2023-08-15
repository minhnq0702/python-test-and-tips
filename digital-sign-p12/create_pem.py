# -*- coding: utf-8 -*-
import datetime
import hashlib

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

# Tạo một cặp khóa RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Tạo một chứng chỉ số self-signed
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "TP. Ho Chi Minh"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, ""),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Cong ty L&A"),
    x509.NameAttribute(NameOID.COMMON_NAME, "l-a.com.vn"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).sign(private_key, hashes.SHA256(), default_backend())

# Chuyển đổi khóa riêng tư và chứng chỉ số thành định dạng PEM
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)

# Ghi khóa riêng tư và chứng chỉ số vào file
private_key_path = "./cert/private_key.pem"
cert_path = "./cert/certificate.pem"

with open(private_key_path, "wb") as private_key_file:
    private_key_file.write(private_key_pem)

with open(cert_path, "wb") as cert_file:
    cert_file.write(cert_pem)
