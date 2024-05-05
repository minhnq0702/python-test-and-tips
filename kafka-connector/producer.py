# -*- coding: utf-8 -*-
from kafka import KafkaProducer


# Thiết lập địa chỉ của Kafka broker (địa chỉ và cổng)
# bootstrap_servers = 'careful-pup-11722-us1-kafka.upstash.io:9092'
# topic_name = 'vcb-exchange-rate'
#
#
#
# # Tạo producer
# producer = KafkaProducer(
#     bootstrap_servers=bootstrap_servers,
#     sasl_mechanism='SCRAM-SHA-256',
#     security_protocol='SASL_SSL',
#     sasl_plain_username='Y2FyZWZ1bC1wdXAtMTE3MjIknsQ0p-AuQRl0WBV28jxM_7GDQDm8Cc5dfY_whP8',
#     sasl_plain_password='NGUyMzMwZDktNDk5Yi00ZDY3LWJjZGEtNmQ1NjFiODFmMTcy',
# )
#
# message = 'Hello, Kafka!!'
# try:
#     print(producer.bootstrap_connected())
#     producer.send(topic_name, message.encode('utf-8'), headers=[('test-upstash', 'test'.encode())])
#     producer.send(topic_name, (message * 2).encode('utf-8'))
#     producer.flush()
# except Exception as e:
#     print('Error: ', e)
# finally:
#     producer.close()
#     print('Closed producer')


class ProducerManager:
    producer = None

    # create singleton producer
    def __new__(cls, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProducerManager, cls).__new__(cls)
            cls.instance.producer = KafkaProducer(
                bootstrap_servers=kwargs['bootstrap_servers'],
                sasl_mechanism=kwargs.get('sasl_mechanism', None),
                security_protocol=kwargs.get('security_protocol', None),
                sasl_plain_username=kwargs.get('sasl_plain_username', None),
                sasl_plain_password=kwargs.get('sasl_plain_password', None)
            )
        return cls.instance

    def send_message(self, topic_name, message):
        try:
            self.producer.send(topic_name, message.encode('utf-8'))
            self.producer.flush()
        except Exception as e:
            print('Error: ', e)
        finally:
            self.producer.close()
            print('Closed producer')


def get_producer(**kwargs):
    return ProducerManager(**kwargs)
