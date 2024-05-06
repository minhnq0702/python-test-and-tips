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
        return func(*args, int(num_of_msg), **kwargs)
    return get_input


@get_producer_inputs
def do_producer(producer: ProducerManager, num_of_msg=1, *args, **kwargs):
    """
    This function will simulate the producer
    :param ProducerManager producer:
    :param num_of_msg:
    :return:
    """
    for _ in range(num_of_msg):
        data = generate_data()
        producer.send_message(KAFKA_TOPIC, data)


if __name__ == '__main__':
    load_env()
    choice = choose_type()
    if choice == '1':
        prod = get_producer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            sasl_mechanism=SASL_MECHANISM,
            security_protocol=SECURITY_PROTOCOL,
            sasl_plain_username=SASL_PLAIN_USERNAME,
            sasl_plain_password=SASL_PLAIN_PASSWORD
        )
        do_producer(prod)
    elif choice == '2':
        cons = get_consumer(
            topic_name=[KAFKA_TOPIC],
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            sasl_mechanism=SASL_MECHANISM,
            security_protocol=SECURITY_PROTOCOL,
            sasl_plain_username=SASL_PLAIN_USERNAME,
            sasl_plain_password=SASL_PLAIN_PASSWORD,
            group_id=KAFKA_CONSUMER_GROUP,
        )
        cons.consume_message()
    else:
        print("Invalid choice")
