#!/usr/bin/env python3
import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a header exchange
channel.exchange_declare(exchange='header_exchange', exchange_type='headers')

# Messages to send with different headers
messages = [
    {
        'body': 'ALERT: Server Overload',
        'headers': {'severity': 'critical', 'source': 'server', 'x-match': 'all'}
    },
    {
        'body': 'INFO: Daily Backup Complete',
        'headers': {'severity': 'info', 'source': 'backup'}
    },
    {
        'body': 'WARNING: High CPU Usage',
        'headers': {'severity': 'warning', 'source': 'monitor'}
    }
]

# Publish messages with headers
for msg in messages:
    channel.basic_publish(
        exchange='header_exchange',
        routing_key='',  # Unused in header exchanges
        body=msg['body'],
        properties=pika.BasicProperties(headers=msg['headers'])
    )
    print(f" [x] Sent: {msg['body']} (Headers: {msg['headers']})")

connection.close()