import pika
import sys


connection=pika.BlockingConnection(parameters=pika.ConnectionParameters('localhost'))
channel=connection.channel()


#1. Exchange
channel.exchange_declare(exchange='direct_logs',exchange_type='direct')

message = {"info":"This is new info","error":"This is new error ❌❌❌","warning":"This is Warning"}
for key,value in message.items():

    channel.basic_publish(exchange='direct_logs', routing_key=key, body=value)

print(f" [x] Sent {message}")
connection.close()
