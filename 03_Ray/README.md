## Ray

---

### Lab - Ray

Just some example of how to use Ray.

### Project
Some stuff running on a docker compose cluster

#### Setup and Run

To run a Ray cluster using this docker-compose file:

- Create a .env file with necessary variables.
- Run docker-compose up.

Then you should be able to run the exercises on the Ray cluster from your local machine.
Just make sure to set the `address` parameter in the `ray.init()` call to the address of the head node of the cluster.
And make sure you are using the same python and ray versions on your local machine as in the docker image.

By default:

- The head node will be accessible at [`localhost:10001`](http://localhost:10001).
- The dashboard will be accessible at [`localhost:8265`](http://localhost:8265).
