import argparse
import random
import time
from threading import Thread

import pika

from config import service_queues


class PublisherThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='SPACE_SERVICES', exchange_type='topic')

        self.name = name

    def run(self):
        while True:
            service = random.choice(service_queues)
            req = f"{service}-{random.randint(1000, 9999)}"
            self.channel.basic_publish(
                exchange='SPACE_SERVICES',
                routing_key=f'request.{self.name}.{service}',
                body=req.encode("utf-8")
            )

            print(f"{self.name}: Sent [{req}]")

            time.sleep(2)

    def __del__(self):
        self.channel.close()
        self.connection.close()
        print(f"{self.name}: Closed connection to the broker")


class SubscriberThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='SPACE_SERVICES', exchange_type='topic')
        self.name = name

    def run(self):
        # exclusive queue for admin messages
        personal_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.queue_bind(exchange='SPACE_SERVICES', queue=personal_queue,
                                routing_key='admin')
        self.channel.basic_consume(
            queue=personal_queue,
            on_message_callback=self.handle_admin_message,
            auto_ack=True
        )

        # shared queue for responses from carriers
        shared_queue = self.channel.queue_declare(queue='RESPONSES', exclusive=False).method.queue
        self.channel.queue_bind(exchange='SPACE_SERVICES', queue=shared_queue,
                                routing_key=f'response.{self.name}.*')

        self.channel.basic_consume(
            queue=shared_queue,
            on_message_callback=self.handle_response,
            auto_ack=True
        )

        self.channel.start_consuming()

    def handle_response(self, channel, method, properties, body):
        print(f"{self.name}: Received: [{body.decode()}]")

    def handle_admin_message(self, channel, method, properties, body):
        print(f"Admin msg: [{body.decode()}]")

    def __del__(self):
        self.channel.close()
        self.connection.close()
        print(f"{self.name}: Closed connection to the broker")


class SpaceAgency:
    def __init__(self, name: str):
        self.name = name

        self.pub = PublisherThread(self.name)
        self.sub = SubscriberThread(self.name)

    def run(self):
        self.pub.start()
        self.sub.start()
        self.pub.join()
        self.sub.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of the agency")
    args = parser.parse_args()

    agency = SpaceAgency(args.name)
    agency.run()
