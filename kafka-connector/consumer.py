# -*- coding: utf-8 -*-
import time

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaError


class ConsumerManager:
    consumer: KafkaConsumer = None
    topic_name = None

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
                    # client_id=f'{_getRandomID}',
                    # auto_offset_reset='earliest',
                    enable_auto_commit=True,
                    # max_poll_interval_ms=300000,  # * default value
                    # session_timeout_ms=50000,
                )
            except NoBrokersAvailable as e:
                print(e)
            except KafkaError as e:
                print(e)
        return cls.instance

    def consume_message(self, delay_time: float = 1, num_of_record: int = 1):
        """
        This function will consume the message from Kafka
        :param float delay_time:  Delay time between each poll action. Default is 1 second
        :param int num_of_record: Number of records you want to consume. Default is 1
        :return:
        """
        try:
            while True:
                print('===> Start consuming message....')
                poll_msg = self.consumer.poll(
                    timeout_ms=500,
                    max_records=num_of_record,
                )
                if poll_msg:
                    for top_partition, msgs in poll_msg.items():
                        print(f'<Topic: {top_partition.topic}/Partition: {top_partition.partition}>')
                        for m in msgs:
                            key = m.key and m.key.decode('utf-8') or ''
                            val = m.value and m.value.decode('utf-8') or ''
                            print(f'==> [Consumed Value]: {key} - {val} / at {m.offset}')

                # * delay
                if delay_time > 0:
                    print(f'===> Waiting for {delay_time} seconds....')
                    time.sleep(delay_time)

        except Exception as e:
            print('Error: ', e)
        finally:
            pass

    def close(self):
        if self.consumer is not None:
            try:
                self.consumer.close()
            except Exception as e:
                print('Error on closing consumer: ', e)

    def __del__(self):
        self.close()


def get_consumer(**kwargs):
    return ConsumerManager(**kwargs)
