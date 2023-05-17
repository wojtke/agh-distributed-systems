## Websockets Chat

---

### Setup

Need python3, should run without any additional packages.

### Run

First run the server with:

```bash
python3 server.py [-p PORT] [-a ADDRESS]
```

Run the client with:

```bash
python3 client.py [-p PORT] [-a ADDRESS] [-m MulticastAddress] [-mp MulticastPort]
```

Client should be able to connect to the server and send messages to other clients via the server.
Used TCP by default, but can send over UDP if '/u <message>' is sent.
Can also send multicast messages with '/m <message>' - these will be sent to all clients connected to the same multicast
group.
