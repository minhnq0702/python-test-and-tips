# -*- coding: utf-8 -*-
import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

import CONST

# Tạo một cặp khóa RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend(),
)

# Tạo một chứng chỉ số self-signed
subject = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, 'Hồ Thị Thu Phượng'),
    x509.NameAttribute(NameOID.LOCALITY_NAME, ''),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'CÔNG TY CỔ PHẦN L&A'),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'THÀNH PHỐ HỒ CHÍ MINH'),
    x509.NameAttribute(NameOID.COUNTRY_NAME, 'VN'),

    x509.NameAttribute(NameOID.TITLE, 'Giám đốc nhân sự'),
    x509.NameAttribute(NameOID.EMAIL_ADDRESS, 'phuong.ho@l-a.com.vn'),
    x509.NameAttribute(NameOID.USER_ID, 'CCCD:025572179'),
])

issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, 'FPT Certification Authority SHA256'),
    x509.NameAttribute(NameOID.LOCALITY_NAME, ''),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, 'FPT Information System'),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'FPT Corporation'),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Hà Nội'),
    x509.NameAttribute(NameOID.COUNTRY_NAME, 'VN'),
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
    encryption_algorithm=serialization.NoEncryption(),
)

cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)

# Ghi khóa riêng tư và chứng chỉ số vào file
private_key_path = CONST.PRIVATE_KEY_PATH
cert_path = CONST.CERT_PATH

with open(private_key_path, 'wb') as private_key_file:
    private_key_file.write(private_key_pem)

with open(cert_path, 'wb') as cert_file:
    cert_file.write(cert_pem)
