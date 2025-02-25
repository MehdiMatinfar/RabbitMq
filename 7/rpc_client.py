import pika
import uuid


class MyRpcClient:
    def __init__(self):
        self.connection=pika.BlockingConnection(parameters=pika.ConnectionParameters('localhost'))
        self.channel=self.connection.channel()
        result=self.channel.queue_declare(queue='', exclusive=True) # the queue which server puts data into it!
        self.queue_name=result.method.queue
        self.channel.basic_consume(queue=self.queue_name,on_message_callback=self.on_respone,auto_ack=True)

    def on_respone(self, ch, method, props, body):
        print(" Waitint " )
        if self.corr_id==props.correlation_id:
            self.response=body
            print(" [x] Received %r" % body)

    def call(self,n):

        self.response=None
        self.corr_id=str(uuid.uuid4())

        # rpc_queue is the queue which client puts data into it!
        # reply_to is where (queue) the server's response comes
        self.channel.basic_publish(exchange='',routing_key='rpc_queue',body=str(n)
                                   ,properties=pika.BasicProperties(correlation_id=self.corr_id,reply_to=self.queue_name))

        # Wait till response receives
        while self.response==None:
            self.connection.process_data_events()
        return int(self.response)

client=MyRpcClient()
client.call(25)