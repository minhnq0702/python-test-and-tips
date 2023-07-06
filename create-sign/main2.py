import hashlib
import hmac
import json
import base64

data = {
    "eKYCId": "eKYCId",
    "phone": "phone",
    "kingcode": "KingCode123",
    "eKYCURL": "https://..."
}

private_key = '-----BEGIN PRIVATE KEY-----\n' \
              'MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDzfy7yV25ZdUdvtQRI2x8oF84Be5+X/b8dfT1l4bu0JXrd+5mjdYUzzwiBqQ5S4psNlKcbLuTH+XEA6WmBlJ1+2LcMPZX+XYu1t6mnGsJbO9WnHIPDJkos5bXI/rKGpsUhslc4MEdzpvk45qmfB5k14snzpaS0RX9caBjjv4qA5biNFQPtcfciMalayB52j2dJ+N4+vAIxlMVNaZryn2+ygGkXoL/1Lidh+jbRm+oKgv2SNMNgkFS9sApkJJZDb+dxRm4PcDBO6H9TiIufZDdJ64ivnWeX6jB4Dr9LHaOcy+OPlK/tz2wtokEhkyX2o/08/vO7/IwqBZrffAJ22Bf1AgMBAAECggEBANs3c5KmeCh915SQSY02CTTVSZg4LhRuVDM+X5prwcuLurRDIazxzrw39haVltm0PZfabx+f9kS7I6uIeH46yBg9D38rqvBYU8GD2m8hPj1Y/x72IwH8ZOdK34BXHW7wkaWmo7Noc8uBVfqOX8NW2e6TgPGj/UZ3ExSke1P/S7iCVynq8Zzd3Bp9fuzfieC/toCxZHYj0jvAcvtZxcrSl0ZvCyLDl3rbv3gI7JFtz08oTzW0ugDYpIT0kmMrdBWlE879P1EiXGfLY6z2/QhsLqkP4FsdLM2RpzLEAJE+ey5O28SRWK05vKRwHxT1BgOLb0VrA5CLG+VbExUKv1+3jIECgYEA/Z/gb0vhQss69Jd+L81oLKJdznsGIYZqLo4A7f6lULVfTTad0d+oI/avdwYV+JpOrxRFnjO3QgJ5QvlFKOeaMi0OI2coZb7ZtzMq9+24PVGMaQraeFTpWtETR2RB7MCZpe973edq3no0WhS3cbMguQBymUIvyZ1lfH2CADoJxVECgYEA9ccF7nRbW8zGBKpNw7juV2/RQd8UH8q3JYft4+f5Yg3XVUzI9BQRqWXbqeiMYy5XqqGiZrGG2KdEmMAEzh5iFtIRt9IgJR0SH/x/ciYRnQJz5E0nWl30Qd6k9HJvHry0bnc/DrkJyR/1J6IqcO5jHvQbFpMt2j77bFnhjaI1j2UCgYAFMYbpAIbGVV8Jryh4Vh5x+4ksNzyy5wu5lFLUjMhZ1Lz02c91grzwr5Z8O3Wrt40w7JtYV/rCsUZGZtBRvBxeNqn5c51SKAxRQgz5Mrb5GnhjlkNO/34fy/Q3HAh1jqQWz8abjqeTkrELvyzaeS6MW0P9e2t7F2wClpdY5ddZYQKBgFjXqpM5yFR0vxesoBOh47YDm3beNp4PXwjYC+wYTJNfQXl6GiHwpzm+shrHDwhDFjl92ACbJ41lWWyF7La9UOPC59i0wh3oVkbttPwEOtWwr0fVg+YslEDDRImAXB6WQ/qybD7cMGddf/blrcXIxlfIEYqlhSuhHK1cCCZ0fjvpAoGBALq2irjA8WIT7GeYjff1cCy8CKwz87NCV5na6wBXip6oEhFh5YH8tfTrU0AkQHf1UkBiG7/N0x0qmXOr4FUJfiV7NCTyKNmB0yRVt1MonSNEqOpHSUXf2qkftA4JODptyEUD4Kp557knKWthk2DOubjNcAgYAUzj8xslNgSsqLT3\n' \
              '-----END PRIVATE KEY-----'

# Chuyển đổi từ điển thành chuỗi JSON
json_data = json.dumps(data)

# Tạo đối tượng hash SHA256 từ chuỗi JSON
sha256_hash = hashlib.sha256(json_data.encode('utf-8'))

# Tạo đối tượng HMAC từ khóa riêng tư và đối tượng hash SHA256
hmac_obj = hmac.new(
    private_key.encode('utf-8'),
    json_data.encode(),
    hashlib.sha256,
)

# Lấy giá trị khóa SHA256 từ đối tượng HMAC
sha256_key = hmac_obj.digest()

print(base64.b64encode(sha256_key))

# NWQyZTZlMzQ4Y2Y5ZmI4MDJmYmVjZDMyZjYyNzlhM2UwN2U3OTgyYmMxYWQxNGI4YjlkZjEzMmZmNGY0ZjNlMw==
# NzQyMDNiNGM4MmYxZTVhNzdmYmY5NWNlMDY3MTM2MDZkYjZlMWU0MGMzMjQ4ZTUzMzUxY2QzOWZlMjQ0ZWY5Yg==
