import random
import time

from config import exchange_name, service_queues
import pika
import argparse


class SpaceAgency:
    def __init__(self, name: str):
        self.name = name

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange="SPACE_SERVICES", exchange_type="topic")

        self.channel.queue_declare(queue="PEOPLE_TRANSPORT")
        self.channel.queue_declare(queue="CARGO_TRANSPORT")
        self.channel.queue_declare(queue="SATELLITE_DEPLOYMENT")

        self.channel.queue_bind(
            exchange=exchange_name,
            queue="PEOPLE_TRANSPORT",
            routing_key="PEOPLE_TRANSPORT",
        )
        self.channel.queue_bind(
            exchange=exchange_name,
            queue="CARGO_TRANSPORT",
            routing_key="CARGO_TRANSPORT",
        )
        self.channel.queue_bind(
            exchange=exchange_name,
            queue="SATELLITE_DEPLOYMENT",
            routing_key="SATELLITE_DEPLOYMENT",
        )

    def run(self):
        while True:
            service = random.choice(service_queues)
            self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=service,
                body=f"{self.name}:{service}".encode("utf-8"),
            )

            print(f"Agency {self.name}: Sent {service} request")

            time.sleep(2)

    def __del__(self):
        self.channel.close()
        print(f"Agency {self.name}: Closed connection to the broker")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of the agency")
    args = parser.parse_args()

    agency = SpaceAgency(args.name)
    agency.run()
