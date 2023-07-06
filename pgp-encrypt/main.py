import pgpy
from pgpy.pgp import PGPKey, PGPUID
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm


def self_create_key():
    pri_key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
    uid = PGPUID.new('L&A Holding', comment='Use for Banking Payment Integrate', email='minhnq.0702@gmail.com')
    # pri_key.pubkey is auto generated public key
    pri_key.add_uid(uid,
                    usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                    hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
                    ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
                    compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed])
    return pri_key, pri_key.pubkey


def get_exists_key():
    pri_key = PGPKey()
    pub_key = PGPKey()
    # with open('./0x32404A4B-sec.asc') as f:
    #     pri_key.parse(f.read())
    #
    # with open('./0x32404A4B-pub.asc') as f:
    #     pub_key.parse(f.read())

    with open('./keys/la_private.asc') as private:
        pri_key.parse(private.read())

    with open('./keys/vcb_public.asc') as public:
        pub_key.parse(public.read())

    pub_key._require_usage_flags = False

    return pri_key, pub_key


# pri, pub = self_create_key()
pri, pub = get_exists_key()


# origin_msg = None
# with open('./new.csv', 'rb') as f:
#     msg = pgpy.PGPMessage.new(f.read())
#     encrypt_res = str(pub.encrypt(msg))
#
# with open('./encrypted.csv', 'w') as f:
#     f.write(encrypt_res)

with open('./ACK_TMP111981_10001746_0000000087_MD_22062023_TESTVCB15_19.encrypt', 'rb') as f, open('./ACK_TMP111981_10001746_0000000087_MD_22062023_TESTVCB15_19.csv', 'w') as e:
    to_decrypt = pgpy.PGPMessage.from_blob(f.read())
    with pri.unlock("Vcb#La@***2023"):
        msg = pri.decrypt(to_decrypt)
        write_msg = msg.message
        print(write_msg)
        if isinstance(write_msg, (bytes, bytearray)):
            write_msg = write_msg.decode('utf-8')
        # if isinstance(write_msg, str):
        #     write_msg = write_msg.encode('utf-8')
        e.write(write_msg)



