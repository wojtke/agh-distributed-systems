## gRPC

---
### Task

#####  A2 - Event Subscription
Develop a client-server application using gRPC for event subscriptions. Clients can subscribe to various event types at the contractor's discretion (e.g., weather conditions, upcoming meetings).

##### Requirements:

- Multiple recipients can subscribe to a single event
- Multiple independent subscriptions allowed
- Use streaming mechanism for communication protocol
- Messages come at varying intervals; assume single-second intervals for demo
- Message definitions should include numeric, enum, string, message fields and a repeated modifier
- Subscription parameters should be included (e.g., city for weather conditions)
##### Implementation:
- Ensure communication is immune to network errors
- Allow re-establishing communication without process restarts
- Cache undelivered messages on the server until connectivity is re-established
- Be "NAT-friendly" (account for address translation)

---
### Setup

Need python3 and node.js. Also need to install gRPC for python and node.js.

Run `. generate.sh` to generate the python server or client code. 
The node.js client generates protobuf code automatically at runtime.

Set up the python server (or client):
```bash
cd server
pip install -r requirements.txt
. generate.sh
```

Set up the node.js client:
```bash
cd client
npm install
```

### Run

Run the server with: 
```bash
python server/server.py
```

Run the node.js client like:
```bash
node client/client.js regular AAPL
```


Run the python client with: 
```bash
python client_py/client.py regular AAPL
```

