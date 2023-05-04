## ZeroC ICE

---
### Task
#####  I3 - Effective Servant Management
Demonstrate Ice technology's servant management mechanism with a simple client-server application. The server side handles multiple Ice objects using dedicated and shared servants.

##### Requirements:

- Two types of middleware objects: dedicated servants for each and shared servants for all
- Efficient servant management (e.g., dedicated servants instantiated only when first requested)
- Simple IDL interface implying a specific servant implementation method (must be justifiable)
- Client application to demonstrate server functionality
- Server-side logs displaying object, servant, request, and instantiation details
- Use Ice technology's native servant management mechanisms
- Middleware objects "reachable" by clients via identifier (Identity)
---


### Setup
Need python3 and java8. Also need to install ZeroC ICE for python and java.

From the root directory of the project run: `
. generate.sh
`
to generate the python and java code from the slice file.

### Run
Run the server with: 
```bash
python3 server/server.py
```

Run the python client with: 
```bash
python3 client_py/client.py
```

Run the java with maven or something. I used IntelliJ.


