# -*- coding: utf-8 -*-
import time

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaError
from kafka.structs import OffsetAndMetadata


class ConsumerManager:
    consumer: KafkaConsumer = None
    bootstrap_servers = None
    topics = None
    auto_offset_reset = 'earliest'
    enable_auto_commit = True
    commit_after_records = 0
    group = None

    def __new__(cls, **kwargs):
        instance = super(ConsumerManager, cls).__new__(cls)
        instance.bootstrap_servers = kwargs['bootstrap_servers']
        instance.topics = kwargs['topics']  # change to .get later
        instance.auto_offset_reset = kwargs.get('auto_offset_reset', 'earliest')
        instance.enable_auto_commit = kwargs.get('enable_auto_commit', True)
        instance.commit_after_records = kwargs.get('commit_after_records', 0)
        instance.group = kwargs.get('group_id', None)

        try:
            instance.consumer = KafkaConsumer(
                *instance.topics,
                bootstrap_servers=instance.bootstrap_servers,
                sasl_mechanism=kwargs.get('sasl_mechanism', None),
                security_protocol=kwargs.get('security_protocol', None),
                sasl_plain_username=kwargs.get('sasl_plain_username', None),
                sasl_plain_password=kwargs.get('sasl_plain_password', None),

                # other options
                group_id=instance.group,
                auto_offset_reset=instance.auto_offset_reset,
                enable_auto_commit=instance.enable_auto_commit,
                # max_poll_interval_ms=300000,  # * default value
                # session_timeout_ms=50000,
                # client_id=f'{_getRandomID}',
                default_offset_commit_callback=lambda x: print(f'====> Offset commit: {x}'),
            )
        except NoBrokersAvailable as e:
            print(e)
        except KafkaError as e:
            print(e)
        else:
            return instance

    def consume_message(self, delay_time: float = 1, num_of_record: int = 1):
        """
        This function will consume the message from Kafka
        :param float delay_time:  Delay time between each poll action. Default is 1 second
        :param int num_of_record: Number of records you want to consume. Default is 1
        :return:
        """
        try:
            read_records = 0
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
                            read_records += 1

                        # * commit offset
                        if not self.enable_auto_commit and self.commit_after_records > 0 and divmod(read_records, self.commit_after_records)[1] == 0:
                            print('doing commit....', read_records)
                            self.manual_commit_offset(top_partition)

                # * delay
                if delay_time > 0:
                    print(f'===> Waiting for {delay_time} seconds....')
                    time.sleep(delay_time)

        except Exception as e:
            print('Error: ', e)
        finally:
            pass

    def manual_commit_offset(self, topic_partition):
        pos = self.consumer.position(topic_partition)
        self.consumer.commit({
            topic_partition: OffsetAndMetadata(pos, time.time())
        })

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
