import pika

from admin import Administrator
from agency import SpaceAgency
from carrier import Carrier
from config import exchange_name, service_queues

# RabbitMQ connection parameters
connection_params = pika.ConnectionParameters(host="localhost")
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Exchange and queues configuration

channel.exchange_declare(exchange=exchange_name, exchange_type="direct")


for queue_name in service_queues.values():
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=queue_name)


# Example usage
if __name__ == "__main__":
    # Create agencies
    agency1 = SpaceAgency("Agency1")
    agency2 = SpaceAgency("Agency2")

    # Create carriers
    carrier1 = Carrier("Carrier1", ["passenger_transport", "cargo_transport"])
    carrier2 = Carrier("Carrier2", ["cargo_transport", "satellite_deployment"])

    # Create administrator
    administrator = Administrator()

    # Send service requests from agencies
    agency1.send_service_request("passenger_transport", "001")
    agency2.send_service_request("satellite_deployment", "002")

    # Process service requests by carriers
    carrier1.process_service_requests()
    carrier2.process_service_requests()

    # Send admin messages
    administrator.send_admin_message("Important message to all agencies", "agencies")
    administrator.send_admin_message("Urgent message to all carriers", "carriers")
    administrator.send_admin_message("General message to all", "all")

# Close the connection
connection.close()
