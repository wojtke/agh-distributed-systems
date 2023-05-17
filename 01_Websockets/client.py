import argparse
import socket
import struct
import time

from server import threaded


class Client:
    def __init__(self, server_host, server_port, multicast_group, multicast_port, nickname):
        self.server_host = server_host
        self.server_port = server_port
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.nickname = nickname

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect((server_host, server_port))

        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_sock.bind(self.tcp_sock.getsockname())
        self.udp_sock.connect((server_host, server_port))

        self.multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.multicast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.multicast_sock.bind((multicast_group, multicast_port))

        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    @threaded
    def listen_tcp(self):
        print(f"Listening for TCP {self.tcp_sock.getsockname()}...")
        time.sleep(0.1)
        while True:
            message = self.tcp_sock.recv(1024)
            if not message:
                continue
            print("\r", message.decode("utf-8"), end="\n> ")

    @threaded
    def listen_udp(self):
        print(f"Listening for UDP {self.udp_sock.getsockname()}...")
        time.sleep(0.1)
        while True:
            message, _ = self.udp_sock.recvfrom(1024)
            if not message:
                continue
            print("\r", message.decode("utf-8"), end="\n> ")

    @threaded
    def listen_multicast(self):
        print(f"Listening for multicast {self.multicast_sock.getsockname()}...")
        time.sleep(0.1)
        while True:
            message, _ = self.multicast_sock.recvfrom(1024)
            if not message:
                continue
            print("\r", message.decode("utf-8"), end="\n> ")

    def run(self):
        self.listen_tcp()
        self.listen_udp()
        self.listen_multicast()
        while True:
            client_input = input("\r> ")

            if not client_input:
                continue
            if client_input.startswith("/"):
                cmd = client_input.split(" ", 1)

                if cmd[0].lower() == "/u":
                    self.udp_sock.sendto(
                        cmd[1].encode("utf-8"),
                        (self.server_host, self.server_port)
                    )

                elif cmd[0].lower() == "/m":
                    self.multicast_sock.sendto(
                        cmd[1].encode("utf-8"),
                        (self.multicast_group, self.multicast_port)
                    )
                else:
                    print("\rUnknown command. Try /u [message], /m [message].", end="\n> ")

            else:
                self.tcp_sock.send(client_input.encode("utf-8"))

            time.sleep(0.1)

    def close(self):
        self.tcp_sock.close()
        self.udp_sock.close()
        self.multicast_sock.close()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-p", "--port", type=int, default=9090)
    args.add_argument("-a", "--address", type=str, default="localhost")
    args.add_argument("-m", "--multicast", type=str, default="224.0.0.123")
    args.add_argument("-mp", "--multicast_port", type=int, default=9091)
    args.add_argument("-n", "--nickname", type=str, default="client")
    args = args.parse_args()
    try:
        client = Client(args.address, args.port, args.multicast, args.multicast_port, args.nickname)
    except ConnectionRefusedError:
        print(f"Cannot connect to server {args.address}:{args.port}. Connection refused.")
        exit()

    try:
        client.run()
    except (KeyboardInterrupt, EOFError):
        client.close()
        exit()
