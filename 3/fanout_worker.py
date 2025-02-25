import pika

# implement all of them for Fanout:
    # 1. implement exchange
    # 2. implement queue
    # 3. implement bindings
    # https://www.rabbitmq.com/tutorials/tutorial-three-python
connection=pika.BlockingConnection(parameters=pika.ConnectionParameters('localhost'))
channel=connection.channel()


#1. Exchange
channel.exchange_declare(exchange='logs',exchange_type='fanout')

#The fanout exchange is very simple.
# As you can probably guess from the name,
# it just broadcasts all the messages it receives to all the queues
# it knows. And that's exactly what we need for our logger.

#random queue


#Secondly, once the consumer connection is closed, the queue should be deleted. There's an exclusive flag for that:
# هر بار که consumer پیام را گرفت ، صف راحذف کرده و دوباره میفرستد
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

print(f"name of queue : {queue_name}")
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

channel.start_consuming()


