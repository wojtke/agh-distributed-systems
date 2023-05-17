import argparse
import socket
import threading
from dataclasses import dataclass
from time import sleep


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
        thread.start()

    return wrapper


@dataclass
class Client:
    tcp_socket: socket.socket
    nick: str = ""

    def send(self, msg):
        self.tcp_socket.send(msg.encode("utf-8"))

    def send_udp(self, msg, udp_socket):
        udp_socket.sendto(msg.encode("utf-8"), self.tcp_socket.getpeername())

    def recv(self):
        while True:
            msg = self.tcp_socket.recv(1024)
            if not msg:
                sleep(0.2)
                continue
            return msg.decode("utf-8")

    def getpeername(self):
        return self.tcp_socket.getpeername()

    def __repr__(self):
        return f"{self.nick}{self.tcp_socket.getpeername()}"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return self.tcp_socket.getpeername() == other.tcp_socket.getpeername()


class Server:
    def __init__(self, host, port):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.tcp_socket.bind((host, port))
        print("TCP server started on port: ", port)

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.udp_socket.bind((host, port))
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("UDP server started on port: ", port)

        self.clients = []

    def run(self):
        self.tcp_socket.listen(5)
        print("Server is listening...")

        self.handle_udp_connection()

        while True:
            sock, addr = self.tcp_socket.accept()
            client = Client(sock)
            self.handle_tcp_connection(client)

    @threaded
    def handle_tcp_connection(self, client):
        self.get_nickname(client)
        self.clients.append(client)
        print(f"Connected: {client}")

        client.send(f"[server] Online users ({len(self.clients)}): {', '.join([c.nick for c in self.clients])}")

        for receiver in self.clients:
            if receiver != client:
                receiver.send(f"[server] {client.nick} joined the chat.")

        try:
            while True:
                msg = client.recv()

                print(f"TCP msg from {client}: {msg}")

                for receiver in self.clients:
                    if receiver != client:
                        receiver.send(f"[{client.nick}] {msg}")

        except ConnectionError:
            print(f"Disconnected: {client}")
            self.clients.remove(client)

    @threaded
    def handle_udp_connection(self):
        while True:
            buff, addr = self.udp_socket.recvfrom(1024)
            msg = buff.decode("utf-8")

            client = [c for c in self.clients if c.getpeername() == addr]
            if not client:
                print(f"UDP msg from unknown client: {msg}")
            else:
                client = client[0]

            print(f"UDP msg from {client}: {msg}")
            for receiver in self.clients:
                if receiver != client:
                    receiver.send_udp(f"[{client.nick}] {msg}", self.udp_socket)

    def get_nickname(self, client: Client):
        client.send("[server] Welcome! Please enter your nickname. ")
        while True:
            msg = client.recv()

            if msg == "server":
                client.send("[server] Nickname cannot be 'server'. ")
                continue

            if not (2 <= len(msg.strip()) <= 20):
                client.send("[server] Nickname must be between 2 and 20 characters. ")
                continue

            if msg in [c.nick for c in self.clients]:
                client.send("[server] Nickname already taken. Please enter another one. ")
                continue

            break

        client.nick = msg

    def stop(self):
        self.tcp_socket.close()
        self.udp_socket.close()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-p", "--port", type=int, default=9090)
    args.add_argument("-a", "--address", type=str, default="localhost")

    args = args.parse_args()

    server = Server(args.address, args.port)
    try:
        server.run()
    except (KeyboardInterrupt, EOFError):
        server.stop()
        print("Server stopped!")
