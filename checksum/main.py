import hashlib
import base64


def create_checksum(file_path):
    """

    :param file_path:
    :return:
    :rtype: str
    """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # for chunk in iter(lambda: f.read(4096), b''):
        #     sha256.update(chunk)
        sha256.update(f.read())
    return sha256.hexdigest()


def create_checksum_file(file_path, cs, upper=False):
    """
    Write file checksum
    :param str file_path:
    :param str cs:
    :param bool upper:
    :return:
    """
    with open(file_path, 'w') as f:
        f.write(cs.upper() if upper else cs)


def compare_checksum_file(file_1, file_2):
    with open(file_1, 'r') as f1:
        cs1 = f1.read()
    with open(file_2, 'r') as f2:
        cs2 = f2.read()
    return cs1 == cs2


if __name__ == '__main__':
    checksum = create_checksum('./TMP111981_0000000087_10001746_MD_19062023_TESTVCB8_12.csv')
    create_checksum_file('./file.checksum', checksum, upper=True)

    print(compare_checksum_file(
        './TMP111981_0000000087_10001746_MD_19062023_TESTVCB8_12.checksum',
        './file.checksum',
    ))

