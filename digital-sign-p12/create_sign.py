# -*- coding: utf-8 -*-
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12

import CONST

# Đường dẫn đến file chứng chỉ số và khóa riêng tư
certificate_path = CONST.CERT_PATH
private_key_path = CONST.PRIVATE_KEY_PATH

# Đọc chứng chỉ số và khóa riêng tư từ file
with open(certificate_path, "rb") as cert_file:
    certificate = x509.load_pem_x509_certificate(
        cert_file.read(),
        default_backend(),
    )

with open(private_key_path, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend(),
    )

# Tạo một đối tượng PKCS12
p12 = serialization.pkcs12.serialize_key_and_certificates(
    name=b"My Certificate",
    key=private_key,
    cert=certificate,
    encryption_algorithm=serialization.BestAvailableEncryption(password=b"1"),
    cas=[certificate]
)

# Ghi đối tượng PKCS12 vào file
p12_path = CONST.P12_PATH
with open(p12_path, "wb") as p12_file:
    p12_file.write(p12)
