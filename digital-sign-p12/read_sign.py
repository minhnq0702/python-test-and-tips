# -*- coding: utf-8 -*-
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

with open('./cert/container.p12', 'rb') as f:
    sign_data = f.read()

p12 = pkcs12.load_key_and_certificates(
    sign_data,
    bytes('1', 'utf-8'),
    backends.default_backend(),
)

key, cert1, cert2 = p12[0], p12[1], p12[2]

print(key)
print(cert1)
print(cert2)


