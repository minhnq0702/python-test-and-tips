import base64
import json
import time
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

from OpenSSL import crypto
from cryptography.hazmat.primitives.asymmetric import utils



def gen_ca(plaintext, path_file_private):
    with open(path_file_private, 'rb') as f:
        pfx_data = f.read()

    p12 = pkcs12.load_pkcs12(pfx_data, b'')
    private_key = p12.key
    cert = p12.cert

    print('==>', private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    ))

    # print(private_key, cert)

    b_text = plaintext.encode('utf-16le')
    # b_text = (
    #     str(time.time()).encode() +
    #     b_text
    #     # cert.certificate.public_bytes(serialization.Encoding.DER)
    # )

    signature = private_key.sign(
        b_text,
        padding=padding.PKCS1v15(),
        algorithm=hashes.SHA1(),
    )

    # Create a CMS signature with the certificate and signature
    # signature = (
    #         # b'\x30' +  # Sequence tag
    #         signature +  # Signature
    #         cert.certificate.public_bytes(serialization.Encoding.DER)  # Certificate
    # )
    # print("Signature:", signature)


    signature_base64 = base64.b64encode(signature).decode('utf-8')
    print("Signature:", signature_base64)

plain_text = 'client_id:2e9d5f1fccc4e086a96c8c574ea17c91&batch_id:274&batch_trace_number:AT-6-T0010&source_account_number:693709&bulk_status:VALD&total_item:3&total_amount:5500000&total_valid_item:3&total_valid_amount:5500000&created_datetime:1688972519000'
path_file_private = './CA_b10.p12'
gen_ca(plain_text, path_file_private)


# import base64
# from Crypto.Signature import pkcs1_15, pss
# from Crypto.Hash import SHA1, SHA256
# from Crypto.PublicKey import RSA
# import OpenSSL.crypto as crypto
#
# def sign_data(data, private_key, cert):
#     private_key = RSA.import_key(private_key)
#
#     h = SHA1.new(
#         data.encode('utf-16le') +
#         cert.certificate.public_bytes(serialization.Encoding.DER))
#
#     # h.update(cert.certificate.public_bytes(serialization.Encoding.DER))
#
#     # signer = pkcs1_15.new(private_key)
#     signer = pss.new(private_key)
#
#     signature = signer.sign(h)
#     # print("\n===>", signature)
#     return base64.b64encode(signature).decode('utf-8')
#
#
# def load_private_key_from_pfx(pfx_path, password):
#     with open(pfx_path, 'rb') as f:
#         pfx_data = f.read()
#     # p12 = crypto.load_pkcs12(pfx_data, password)
#     p12 = pkcs12.load_pkcs12(pfx_data, password.encode())
#     # private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
#     private_key = p12.key.private_bytes(
#         serialization.Encoding.PEM,
#         serialization.PrivateFormat.TraditionalOpenSSL,
#         serialization.NoEncryption()
#     )
#     # print(private_key)
#     return private_key, p12.cert
#
# # Thông tin cần thiết
# plain_text = 'client_id:2e9d5f1fccc4e086a96c8c574ea17c91&batch_id:274&batch_trace_number:AT-6-T0010&source_account_number:693709&bulk_status:VALD&total_item:3&total_amount:5500000&total_valid_item:3&total_valid_amount:5500000&created_datetime:1688972519000'
# path_file_private = './CA_b10.p12'
# password = ''
#
# # Tạo chữ ký
# private_key, cert = load_private_key_from_pfx(path_file_private, password)
# signature = sign_data(plain_text, private_key, cert)
#
# print("Signature:", signature)


