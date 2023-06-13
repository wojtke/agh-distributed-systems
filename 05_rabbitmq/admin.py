from config import exchange_name
import pika
from threading import Thread


class Administrator:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue="admin_queue")
        self.channel.queue_bind(exchange=exchange_name, queue="admin_queue", routing_key="admin_queue")
        self.channel.basic_consume(
            queue="admin_queue",
            on_message_callback=self.handle_admin_message,
            auto_ack=True,
        )

    def cli(self):
        while True:
            print("Enter message to send to all agencies:")
            message = input(">")
            self.channel.basic_publish(exchange=exchange_name, routing_key="admin_queue", body=message.encode())

    def run(self):
        Thread(target=self.cli).start()
        self.channel.start_consuming()

    def handle_admin_message(self, channel, method, properties, body):
        print(f"Administrator: Received admin message: {body.decode()}")

    def __del__(self):
        self.channel.close()
        self.connection.close()
        print("Administrator: Closed connection to the broker")


if __name__ == "__main__":
    administrator = Administrator()
    administrator.run()

