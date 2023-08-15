# -*- coding: utf-8 -*-
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Đường dẫn đến file chứng chỉ số và khóa riêng tư
certificate_path = "path/to/certificate.crt"
private_key_path = "path/to/private_key.key"

# Đọc chứng chỉ số và khóa riêng tư từ file
with open(certificate_path, "rb") as cert_file:
    certificate = x509.load_pem_x509_certificate(cert_file.read(), default_backend())

with open(private_key_path, "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

# Tạo một đối tượng PKCS12
p12 = serialization.pkcs12.serialize_key_and_certificates(
    name="My Certificate",
    key=private_key,
    cert=certificate,
    encryption_algorithm=serialization.NoEncryption()
)

# Ghi đối tượng PKCS12 vào file
p12_path = "path/to/output.p12"
with open(p12_path, "wb") as p12_file:
    p12_file.write(p12)
