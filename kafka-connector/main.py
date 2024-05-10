# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
import functools

from producer import get_producer, ProducerManager
from consumer import get_consumer, ConsumerManager
from fake import generate_data


KAFKA_BOOTSTRAP_SERVERS = None
KAFKA_TOPIC = None
KAFKA_CONSUMER_GROUP = None
SASL_MECHANISM = None
SECURITY_PROTOCOL = None
SASL_PLAIN_USERNAME = None
SASL_PLAIN_PASSWORD = None


def load_env():
    load_dotenv('./.env')
    global KAFKA_BOOTSTRAP_SERVERS
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')

    global KAFKA_TOPIC
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

    global KAFKA_CONSUMER_GROUP
    KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP')

    global SASL_MECHANISM
    SASL_MECHANISM = os.getenv('SASL_MECHANISM')

    global SECURITY_PROTOCOL
    SECURITY_PROTOCOL = os.getenv('SECURITY_PROTOCOL')

    global SASL_PLAIN_USERNAME
    SASL_PLAIN_USERNAME = os.getenv('SASL_PLAIN_USERNAME')

    global SASL_PLAIN_PASSWORD
    SASL_PLAIN_PASSWORD = os.getenv('SASL_PLAIN_PASSWORD')


def choose_type():
    print("Choose the type of the Kafka you want to simulate:")
    print("1. Producer")
    print("2. Consumer")
    k_choice = input("Enter your choice: ")
    return k_choice


def get_producer_inputs(func):
    # ! use decorator here just for  fun ^_^
    @functools.wraps(func)
    def get_input(*args, **kwargs):
        num_of_msg = input('Enter the number of messages you want to send: ')
        return func(args[0], int(num_of_msg), *args[1:], **kwargs)
    return get_input


def get_consumer_inputs(func):
    # ! use decorator here just for  fun ^_^
    @functools.wraps(func)
    def get_input(*args, **kwargs):
        num_of_record = None
        while not num_of_record or not num_of_record.isnumeric():
            num_of_record = input('Enter the number of messages you want to consume: ')

        delay_time = None
        while not delay_time or not delay_time.isnumeric():
            delay_time = input('Enter the delay time between each poll action: ')

        kwargs['num_of_record'] = int(num_of_record)
        kwargs['delay_time'] = float(delay_time)
        return func(*args, **kwargs)
    return get_input


@get_producer_inputs
def do_produce(producer: ProducerManager, num_of_msg=1, *args, **kwargs):
    """
    This function will simulate the producer
    :param ProducerManager producer:
    :param num_of_msg:
    :return:
    """
    for _ in range(num_of_msg):
        data = generate_data()
        producer.send_message(KAFKA_TOPIC, data)


@get_consumer_inputs
def do_consume(consumer: ConsumerManager, delay_time: float = 1.0, num_of_record: int = 1, *args, **kwargs):
    """
    This function will simulate the consumer
    :param consumer:
    :param delay_time:
    :param num_of_record:
    :param kwargs:
    :return:
    """
    consumer.consume_message(delay_time, num_of_record)


if __name__ == '__main__':
    load_env()
    choice = choose_type()
    try:
        if choice == '1':
            prod = get_producer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                sasl_mechanism=SASL_MECHANISM,
                security_protocol=SECURITY_PROTOCOL,
                sasl_plain_username=SASL_PLAIN_USERNAME,
                sasl_plain_password=SASL_PLAIN_PASSWORD
            )
            do_produce(prod)
        elif choice == '2':
            auto_commit = None
            while auto_commit not in ['y', 'n']:
                auto_commit = input('Do you want to auto commit the offset? (y/n): ').lower()

            commit_after_records = None
            if auto_commit == 'n':
                while not commit_after_records or not commit_after_records.isnumeric():
                    commit_after_records = input('Enter the number of records to commit the offset: ')

            auto_offset_reset = None
            while auto_offset_reset not in ['earliest', 'latest', 'none']:
                auto_offset_reset = input('Enter the auto offset reset (earliest/latest/none): ')

            cons = None
            while cons is None:
                cons = get_consumer(
                    topics=[KAFKA_TOPIC],
                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                    sasl_mechanism=SASL_MECHANISM,
                    security_protocol=SECURITY_PROTOCOL,
                    sasl_plain_username=SASL_PLAIN_USERNAME,
                    sasl_plain_password=SASL_PLAIN_PASSWORD,
                    auto_offset_reset=auto_offset_reset,
                    enable_auto_commit=True if auto_commit == 'y' else False,
                    commit_after_records=int(commit_after_records) if commit_after_records else 0,
                    group_id=KAFKA_CONSUMER_GROUP,
                )
                if cons is None:
                    input('Init consumer failed. Press any key to retry...')

            do_consume(cons)
        else:
            print("Invalid choice")
    except KeyboardInterrupt:
        print('Exiting....')
        exit(0)
