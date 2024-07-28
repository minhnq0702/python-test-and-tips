import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.auth import HTTPBasicAuth

from twilio.rest import Client

# test
to_number = '+84982574806'
from_number = '+15005550006'
body = 'SMS Twilio test'

def create_client():
    # test credentials
    account_sid = 'xxx'
    auth_token = 'yyy'
    _client = Client(account_sid, auth_token)
    return _client
client = create_client()


def send_sms_normal(_client: Client, to_number, from_number, body):
    message = _client.messages.create(
        body=body,
        from_=from_number,
        to=to_number
    )
    print(f'SMS sent successfully, message SID: {message.sid}')


def send_sms_fire_and_forget(_client: Client, to_number, from_number, body, _callback, _index):
    def _send_sms():
        start = time.time()
        message = _client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        print(f'{_index}:--- SMS sent successfully, message SID: {message.sid} / Time: {time.time() - start} seconds')
        # _callback(threading.current_thread())

    def _send_by_http():
        start = time.time()
        account_sid = 'xxx'
        auth_token = 'yyy'

        # Your Twilio number and the recipient's number
        _to_number = '+84982574806'
        _from_number = '+18284265622'

        # The message to send
        _body = 'Hello, this is a message from Twilio!'

        # The URL for the Twilio Messages API
        url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'

        # The data to send with the POST request
        data = {
            'From': _from_number,
            'To': _to_number,
            'Body': _body,
        }

        # Make the POST request
        try:
            response = requests.post(url, data=data, auth=HTTPBasicAuth(account_sid, auth_token))
        except requests.HTTPError as e:
            print(f'{threading.current_thread()}:--- Error sending SMS: {e}')
        except requests.RequestException as e:
            pass
            # print(f'{threading.current_thread()}:--- Error sending SMS: {e}')
        else:
            print(f'{threading.current_thread()}:--- SMS sent successfully, message SID: {response.json().get("sid")} / Time: {time.time() - start} seconds')
        _callback(threading.current_thread())

    with semaphore:
        _send_sms()
        # _send_by_http()



# * Test send sms normal
start_time = time.time()
send_sms_normal(client, to_number, from_number, body)
end_time = time.time()
print(f'Normal method took {end_time - start_time} seconds')


MAX_THREAD = 40
NUM_SMS = 100000
semaphore = threading.Semaphore(MAX_THREAD)

start_time = time.time()
# generate 20 threads poll to send sms
tasks = []
res = []


def callback(val):
    res.append(val)
    pass


with ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
    futures = [executor.submit(
        send_sms_fire_and_forget, client, to_number, from_number, body, callback, i
    ) for i in range(NUM_SMS)]

    # Chờ tất cả các thread hoàn thành
    # for future in futures:
    #     future.result()

# for i in range(100):
#     t = threading.Thread(name=f'worker-{i}', target=send_sms_fire_and_forget, args=(client, to_number, from_number, body, callback))
#     tasks.append(t)
#     # send_sms_fire_and_forget(to_number, from_number, body)
#     t.start()
# for t in tasks:
#     t.join()

end_time = time.time()
print(f'Fire-and-forget method took {end_time - start_time} seconds', res)
