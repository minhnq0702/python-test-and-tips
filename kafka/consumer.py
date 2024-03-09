import kafka
from kafka import KafkaConsumer
from kafka.structs import TopicPartition

import logging

logging.basicConfig(level=logging.DEBUG)


# Thiết lập địa chỉ của Kafka broker (địa chỉ và cổng)
bootstrap_servers = ['localhost:9092']
topic_name = ['dev_1']

heartbeat_interval_ms = 1000
session_timeout_ms = 50000

con1 = KafkaConsumer(
    # topic_name,
    bootstrap_servers=bootstrap_servers,
    # request_timeout_ms=300000,
    # session_timeout_ms=session_timeout_ms,
    # heartbeat_interval_ms=heartbeat_interval_ms,
    # enable_auto_commit=True,
    group_id='test-group-1',
    client_id='client-1',
)

con2 = KafkaConsumer(
    # topic_name,
    bootstrap_servers=bootstrap_servers,
    # request_timeout_ms=300000,
    # session_timeout_ms=session_timeout_ms,
    # heartbeat_interval_ms=heartbeat_interval_ms,
    # enable_auto_commit=True,
    group_id='test-group-1',
    client_id='client-2',
)

con1.subscribe(topic_name)
con2.subscribe(topic_name)

# print("is connected?", cons.bootstrap_connected())
# print("topics?", cons.topics())
# print("is subscribed?", cons.subscription())
# print("is assignment?", cons.assignment())

while True:
    try:
        for cons in [con1, con2]:
            print('====>start', cons.bootstrap_connected())
            try:
                msg = cons.poll(timeout_ms=2000, max_records=1)
                if msg:
                    for top_partition, msgs in msg.items():
                        print('TOPIC:', top_partition.topic)
                        print('PARTITION:', top_partition.partition)
                        for m in msgs:
                            print('OFFSET:', m.offset)
                            print('KEY:', m.key.decode('utf-8'))
                            val = m.value.decode('utf-8')
                            print('VALUE:', val)

                print('====>end')
            except Exception as e:
                print('Error:', e)
    except:
        print('Error and has nothing')
        break

