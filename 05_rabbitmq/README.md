## RabbitMQ

---
### Task


The task involves implementing, using RabbitMQ, a mediator system between space agencies (Agencies) and space transportation service providers (Carriers). Space agencies commission three types of services: passenger transportation, cargo transportation, and satellite placement in orbit.

##### Requirements:

- The prices for each service are the same for all Carriers and are not considered in the system.
- Each Carrier provides exactly two out of the three types of services, specifying which two types they offer when entering into cooperation.
- A specific service request should be assigned to the first available Carrier that handles that type of request.
- A request cannot be assigned to more than one Carrier.
- Requests are identified by the Agency's name and an internal request number assigned by the Agency.
- After providing the service, the Carrier sends a confirmation to the Agency.

In the premium version of the system, an additional administrative module is available. The administrator receives copies of all messages sent in the system and can send messages in three modes:
- To all Agencies
- To all Carriers
- To all Agencies and Carriers


### Setup
Get some rabbitmq server running. It is easy with docker.
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```

Python3 is needed. Also need to install pika.
```bash
pip3 install -r requirements.txt
```

### Run
Run the agency with: 
```bash
python3 agency.py <agency_name>
```

Run the carrier with: 
```bash
python3 carrier.py <carrier_name> [-p] [-c] [-s]
```
- -p for passenger transport
- -c for cargo transport 
- -s for satellite deployment


Run the admin with: 
```bash
python3 admin.py
```





