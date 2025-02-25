import pika
import json

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='example_queue', durable=True)

# Message body
message_body = {
    "order_id": 12345,
    "status": "created"
}

# Message properties
properties = pika.BasicProperties(
    content_type='application/json',  # Content type
    content_encoding='utf-8',        # Encoding
    headers={'x-custom-header': 'value'},  # Custom headers
    delivery_mode=2,  # Persistent message
    priority=5,       # Message priority
    correlation_id='12345',  # Correlation ID
    reply_to='reply_queue',  # Reply queue
    expiration='60000',  # TTL in milliseconds
    message_id='msg_12345',  # Message ID
    timestamp=pika.spec.Timestamp(1697049600),  # Timestamp
    type='order.created',  # Message type
    user_id='admin',  # User ID
    app_id='order_service'  # App ID
)

# Publish the message
channel.basic_publish(
    exchange='',
    routing_key='example_queue',
    body=json.dumps(message_body),
    properties=properties
)

print("Message published with properties!")
connection.close()