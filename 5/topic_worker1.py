import pika


connection=pika.BlockingConnection(parameters=pika.ConnectionParameters('localhost'))
channel=connection.channel()


channel.exchange_declare(exchange='topic_logs',exchange_type='topic')


result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

print(f"name of queue : {queue_name}")
binding_key="*.*.important"

channel.queue_bind(exchange='topic_logs',routing_key=binding_key,queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

channel.start_consuming()


