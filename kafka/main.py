import time

from kafka import KafkaProducer, KafkaClient


# Thiết lập địa chỉ của Kafka broker (địa chỉ và cổng)
bootstrap_servers = 'localhost:9092'
topic_name = 'dev_1'

# client = KafkaClient(bootstrap_servers=bootstrap_servers)
# client.add_topic(topic=topic_name)
# client.poll()

# Tạo producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

message = 'Hello, Kafka!!'
try:
    print(producer.bootstrap_connected())
    producer.send(topic_name, message.encode('utf-8'), key='dev'.encode('utf-8'))
    producer.send(topic_name, (message * 2).encode('utf-8'), key='dev'.encode('utf-8'))

    producer.flush()
except Exception as e:
    print('Error: ', e)
