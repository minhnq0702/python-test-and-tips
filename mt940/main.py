import mt940
import pprint

# Đọc file MT940
with open("./test.mt940", "r") as f:
    data = f.read()

# Phân tích dữ liệu MT940
messages = mt940.parse(data)

# In ra thông tin các giao dịch
print('==>', messages.data)
for message in messages:
    print('==>', message)
    for transaction in message.transactions:
        pprint.pprint(transaction.data)
        print('==>', transaction.data['amount'].data)
        # print("Ngày giao dịch:", transaction.date)
        # print("Số tiền:", transaction.amount)
        # print("Mô tả:", transaction.description)
