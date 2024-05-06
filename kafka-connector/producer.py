# -*- coding: utf-8 -*-
from kafka import KafkaProducer


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

    def send_message(self, topic_name: str, message: str):
        try:
            self.producer.send(topic_name, message.encode('utf-8'))
            self.producer.flush()
        except Exception as e:
            print('Error: ', e)
        finally:
            pass

    def close(self):
        if self.producer is not None:
            self.producer.close()

    def __del__(self):
        self.close()


def get_producer(**kwargs):
    return ProducerManager(**kwargs)
