import argparse
import time

import pika


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

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='SPACE_SERVICES', exchange_type='topic')

        self.queue = self.channel.queue_declare(queue='', exclusive=True).method.queue

    def run(self):
        self.channel.queue_bind(exchange='SPACE_SERVICES', queue=self.queue, routing_key='admin')
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.handle_admin_message,
            auto_ack=True
        )

        if self.people_transport:
            q = self.channel.queue_declare(queue='PEOPLE_TRANSPORT', exclusive=False).method.queue
            self.channel.queue_bind(exchange='SPACE_SERVICES', queue=q,
                                    routing_key='request.*.PEOPLE_TRANSPORT')

            self.channel.basic_consume(
                queue=q,
                on_message_callback=self.handle_service_request,
                auto_ack=False
            )
        if self.cargo_transport:
            q = self.channel.queue_declare(queue='CARGO_TRANSPORT', exclusive=False).method.queue
            self.channel.queue_bind(exchange='SPACE_SERVICES', queue=q,
                                    routing_key='request.*.CARGO_TRANSPORT')

            self.channel.basic_consume(
                queue=q,
                on_message_callback=self.handle_service_request,
                auto_ack=False
            )
        if self.satellite_deployment:
            q = self.channel.queue_declare(queue='SATELLITE_DEPLOYMENT', exclusive=False).method.queue
            self.channel.queue_bind(exchange='SPACE_SERVICES', queue=q,
                                    routing_key='request.*.SATELLITE_DEPLOYMENT')

            self.channel.basic_consume(
                queue=q,
                on_message_callback=self.handle_service_request,
                auto_ack=False
            )

        self.channel.basic_qos(prefetch_count=1)
        self.channel.start_consuming()

    def handle_admin_message(self, channel, method, properties, body):
        print(f"Admin msg: [{body.decode()}]")

    def handle_service_request(self, channel, method, properties, body):
        print(f"{self.name}: Received message [{body.decode()}]")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(1)

        agency_name = method.routing_key.split('.')[1]
        service = method.routing_key.split('.')[2]
        res = body.decode("utf-8") + " handled by " + self.name
        self.channel.basic_publish(
            exchange='SPACE_SERVICES',
            routing_key=f'response.{agency_name}.{service}',
            body=res.encode("utf-8")
        )

        print(f"{self.name}: Sent response [{res}] to {agency_name}")

    def __del__(self):
        self.channel.close()
        print(f"{self.name}: Closed connection to the broker")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("-p", "--people", action="store_true")
    parser.add_argument("-c", "--cargo", action="store_true")
    parser.add_argument("-s", "--satellite", action="store_true")
    args = parser.parse_args()

    carrier = Carrier(args.name, args.people, args.cargo, args.satellite)
    carrier.run()
