# -*- coding: utf-8 -*-
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaError


# Thiết lập địa chỉ của Kafka broker (địa chỉ và cổng)
# bootstrap_servers = ['careful-pup-11722-us1-kafka.upstash.io:9092']
# topic_name = ['vcb-exchange-rate']
#
# heartbeat_interval_ms = 1000
# session_timeout_ms = 50000


# con2 = KafkaConsumer(
#     # topic_name,
#     bootstrap_servers=bootstrap_servers,
#     request_timeout_ms=300000,
#     session_timeout_ms=session_timeout_ms,
#     heartbeat_interval_ms=heartbeat_interval_ms,
#     enable_auto_commit=True,
#     group_id='test-group-1',
#     client_id='client-2',
# )

# con1.subscribe(topic_name)
# con2.subscribe(topic_name)

# print("is connected?", cons.bootstrap_connected())
# print("topics?", cons.topics())
# print("is subscribed?", cons.subscription())
# print("is assignment?", cons.assignment())

# while True:
#     try:
#         for cons in [con1]:
#             print('====>start', cons.bootstrap_connected())
#             try:
#                 msg = cons.poll(timeout_ms=2000, max_records=1)
#                 if msg:
#                     for top_partition, msgs in msg.items():
#                         print('TOPIC:', top_partition.topic)
#                         print('PARTITION:', top_partition.partition)
#                         for m in msgs:
#                             print('OFFSET:', m.offset)
#                             print('KEY:', m.key.decode('utf-8'))
#                             val = m.value.decode('utf-8')
#                             print('VALUE:', val)
#
#                 print('====>end')
#             except Exception as e:
#                 print('Error:', e)
#     except:
#         print('Error and has nothing')
#         break


class ConsumerManager:
    consumer = None

    # create singleton consumer
    def __new__(cls, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConsumerManager, cls).__new__(cls)
            try:
                cls.instance.consumer = KafkaConsumer(
                    *kwargs.get('topic_name', []),
                    bootstrap_servers=kwargs['bootstrap_servers'],
                    sasl_mechanism=kwargs.get('sasl_mechanism', None),
                    security_protocol=kwargs.get('security_protocol', None),
                    sasl_plain_username=kwargs.get('sasl_plain_username', None),
                    sasl_plain_password=kwargs.get('sasl_plain_password', None),

                    # other options
                    group_id=kwargs.get('group_id', None),
                    # client_id=f'{self.db_name}-{self.db_id}',
                    auto_offset_reset='earliest',
                    # enable_auto_commit=True,
                    max_poll_records=kwargs.get('max_poll_records', 1),
                    # max_poll_interval_ms=300000,  # * default value
                    # session_timeout_ms=50000,
                )
            except NoBrokersAvailable as e:
                print(e)
            except KafkaError as e:
                print(e)
        return cls.instance

    def consume_message(self):
        try:
            print('Start consuming message')
            msgs = self.consumer.poll(
                timeout_ms=500,
                # max_records=1,
            )
            if msgs:
                for msg in msgs:
                    print(msg)
        except Exception as e:
            print('Error: ', e)
        finally:
            pass

    def close(self):
        if self.consumer is not None:
            self.consumer.close()
            print('Closed consumer')

    def __del__(self):
        self.close()


def get_consumer(**kwargs):
    return ConsumerManager(**kwargs)
