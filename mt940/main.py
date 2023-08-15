import mt940
import pprint

# Đọc file MT940
with open("./0211006868888 18012021.mt940", "r") as f:
    data = f.read()

# Phân tích dữ liệu MT940
messages = mt940.parse(data)
print('message', messages)

# In ra thông tin các giao dịch
pprint.pprint(messages.data)
for message in messages.transactions:
    pprint.pprint('==> %s' % message.data)
    # for transaction in message.transactions:
    #     pprint.pprint(transaction)
    #     # print('==>', transaction.data['amount'].data)
    #     print('===>', transaction.data['transaction_details'])
    #     # print("Ngày giao dịch:", transaction.date)
    #     # print("Số tiền:", transaction.amount)
    #     # print("Mô tả:", transaction.description)
