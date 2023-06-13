import time

from config import service_queues
import pika
import argparse


class Carrier:
    def __init__(
        self,
        name: str,
        people_transport: bool,
        cargo_transport: bool,
        satellite_deployment: bool,
    ):
        self.name = name

        self.people_transport = people_transport
        self.cargo_transport = cargo_transport
        self.satellite_deployment = satellite_deployment

        self.channel = pika.BlockingConnection(pika.ConnectionParameters(host="localhost")).channel()

    def run(self):
        if self.people_transport:
            self.channel.queue_declare(queue="PEOPLE_TRANSPORT")
            self.channel.basic_consume(
                queue="PEOPLE_TRANSPORT",
                on_message_callback=self.handle_people_transport,
            )

        if self.cargo_transport:
            self.channel.queue_declare(queue="CARGO_TRANSPORT")
            self.channel.basic_consume(
                queue="CARGO_TRANSPORT",
                on_message_callback=self.handle_cargo_transport,
            )

        if self.satellite_deployment:
            self.channel.queue_declare(queue="SATELLITE_DEPLOYMENT")
            self.channel.basic_consume(
                queue="SATELLITE_DEPLOYMENT",
                on_message_callback=self.handle_satellite_deployment,
            )

        self.channel.start_consuming()

    def handle_people_transport(self, channel, method, properties, body):
        print(f"Carrier {self.name}: Received people transport request {body.decode()}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(2)

    def handle_cargo_transport(self, channel, method, properties, body):
        print(f"Carrier {self.name}: Received cargo transport request {body.decode()}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(2)

    def handle_satellite_deployment(self, channel, method, properties, body):
        print(f"Carrier {self.name}: Received satellite deployment request {body.decode()}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(2)

    def __del__(self):
        self.channel.close()
        print(f"Carrier {self.name}: Closed connection to the broker")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("-p", "--people", action="store_true")
    parser.add_argument("-c", "--cargo", action="store_true")
    parser.add_argument("-s", "--satellite", action="store_true")
    args = parser.parse_args()

    carrier = Carrier(args.name, args.people, args.cargo, args.satellite)
    carrier.run()
