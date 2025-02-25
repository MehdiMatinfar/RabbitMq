#!/usr/bin/env python3
import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the header exchange
channel.exchange_declare(exchange='header_exchange', exchange_type='headers')

# Create an exclusive queue
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind the queue to the exchange with specific headers
# This consumer listens for messages with EITHER 'severity=critical' OR 'source=backup'
channel.queue_bind(
    exchange='header_exchange',
    queue=queue_name,
    arguments={
        'severity': 'critical',
        'source': 'backup',
        'x-match': 'any'  # Match ANY of the headers
    }
)

print(' [*] Waiting for messages. To exit, press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")
    print(f"     Headers: {properties.headers}\n")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

channel.start_consuming()