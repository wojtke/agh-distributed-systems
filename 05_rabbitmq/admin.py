import time
from threading import Thread

import pika

from config import exchange_name


class PublisherThread(Thread):
    def __init__(self, routing_key, message):
        Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='SPACE_SERVICES', exchange_type='topic')

        self.routing_key = routing_key
        self.message = message

    def run(self):
        while True:
            self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=self.routing_key,
                body=self.message.encode("utf-8")
            )
            time.sleep(5)


class SubscriberThread(Thread):
    def __init__(self, routing_key):
        Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='SPACE_SERVICES', exchange_type='topic')

        self.routing_key = routing_key

    def run(self):
        queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.queue_bind(exchange=exchange_name, queue=queue, routing_key=self.routing_key)
        self.channel.basic_consume(queue=queue, on_message_callback=self.handle_message, auto_ack=True)
        self.channel.start_consuming()

    def handle_message(self, channel, method, properties, body):
        print(f"Received message: {body.decode()}")


class Administrator:
    def __init__(self):
        self.pub = PublisherThread("admin", "some admin message")
        self.sub = SubscriberThread("#")

    def run(self):
        self.pub.start()
        self.sub.start()
        self.pub.join()
        self.sub.join()


if __name__ == "__main__":
    administrator = Administrator()
    administrator.run()
