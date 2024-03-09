import json

from cryptography import fernet
import base64
import openpyxl
import pandas
from io import BytesIO


# should read key from file
# key = fernet.Fernet.generate_key()
with open('./secret.key', 'rb') as file:
    key = file.read()
    print(key)


def encrypt_file():
    if key:
        try:
            cipher = fernet.Fernet(key)
            with open('TEMPLATE PAYROLL BINH MINH (2).xlsx', 'rb') as f:
                file_base64 = base64.b64encode(f.read())
                encrypt_file = cipher.encrypt(file_base64)
            with open('encrypt.tmp', 'wb') as f:
                f.write(encrypt_file)
                f.seek(0)

        except:
            pass


def decrypt_file():
    if key:
        cipher = fernet.Fernet(key)
        try:
            with open('evaluate_file.tmp', 'rb') as f:
                decrypted_file = cipher.decrypt(f.read())
                # print(decrypted_file)
                wb = openpyxl.load_workbook(BytesIO(base64.b64decode(decrypted_file)))
            with open('new.xlsx', 'wb') as f:
                wb.save(f)
                f.seek(0)
        except Exception as e:
            print('Loi roi', e)
            pass

        try:
            with open('evaluate_json.tmp', 'rb') as f:
                decrypted_json = cipher.decrypt(f.read())
                # print(decrypted_json.decode())
            with open('new.json', 'w') as f:
                f.write(json.dumps(eval(decrypted_json.decode()), ensure_ascii=False))
        except Exception as e:
            print('Loi roi 2', e)
            pass


if __name__ == '__main__':
    # encrypt_file()
    decrypt_file()
