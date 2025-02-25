import pika
import sys


connection=pika.BlockingConnection(parameters=pika.ConnectionParameters('localhost'))
channel=connection.channel()


#1. Exchange
channel.exchange_declare(exchange='topic_logs',exchange_type='topic')

message = {"info.data.important":"This is new info","info.manage.important":"This is new error ❌❌❌","info.notimportant":"This is Warning"}
for key,value in message.items():

    channel.basic_publish(exchange='topic_logs', routing_key=key, body=value)

print(f" [x] Sent {message}")
connection.close()
