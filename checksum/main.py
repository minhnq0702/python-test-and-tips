import hashlib
import base64

sha256 = hashlib.sha256()
with open('./TMP111981_0000000087_10001746_MD_19062023_TESTVCB8_12.csv', 'rb') as f:
    # for chunk in iter(lambda: f.read(4096), b''):
    #     sha256.update(chunk)
    sha256.update(f.read())


with open('./test.checksum', 'w') as f:
    f.write(sha256.hexdigest().upper())
