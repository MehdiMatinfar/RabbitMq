import pika
import sys

# implement all of them for Fanout:
    # 1. implement exchange
    # 2. implement queue
    # 3. implement bindings
    # https://www.rabbitmq.com/tutorials/tutorial-three-python
connection=pika.BlockingConnection(parameters=pika.ConnectionParameters('localhost'))
channel=connection.channel()


#1. Exchange
channel.exchange_declare(exchange='logs',exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(f" [x] Sent {message}")
connection.close()
