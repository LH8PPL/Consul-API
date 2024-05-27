# Consul-API Exercise solution
A 1-node Consul cluster on Vagrant with Python Flask Api service that checks Consul API endpoints.
## Pre-requisites
Setting this up on your local machine assumes the following pre-requisities:

- Hashicorp Vagrant
- Oracle Virtualbox
- git client
- Docker

## Cluster Architecture
The `Vagrantfile` is set up to create a 1 small VM (1 vCPU, 1G memory) running Ubuntu, has Consul server installed.

The `Dockerfile` under api_service folder, that runs the API application.

## Usage
### Download the Repo first

	git clone https://github.com/LH8PPL/Consul-API.git

### Change the directory to the Repo folder

	cd Consul-API

### Consul Cluster Creation
```
# Create the Consul server to bootstrap the Consul cluster
vagrant up 

# open up another terminal and log on to the consul01 server to see the Consul cluster converge.
vagrant ssh consul01

# On the Consul server, see the membership list by running "consul members".
consul members

# OPTIONAL: Destroy the Consul server (since it's outlived it usefulness in this setup)
vagrant destroy
```
### Quick check if everything works

Once the provisioning is over, you should be able to connect via http://localhost:8500 for consul UI and http://127.0.0.1:8500/v1/agent/self for consul API .

### Run the api service
    # Change the directory to the api_service folder:
    cd api_service

    # Build the Docker image:
    docker build -t consul-api-service .

    # Run the Docker container:
    docker run -d -p 5000:5000 consul-api-service

With this, the api service should be up and running. To confirm everything works, you can point your browser to http://127.0.0.1:5000/swagger-ui and see Swagger documentation rendered out! and http://127.0.0.1:5000/ for the Endpoints:

| Endpoint | Description |
|----------|-------------|
| `/v1/api/consulCluster/status` | Check the status of the Consul server. |
| `/v1/api/consulCluster/summary` | Get a summary of the Consul cluster. |
| `/v1/api/consulCluster/members` | Get the list of registered nodes. |
| `/v1/api/consulCluster/systemInfo` | Get system information about the Docker container. |

### Simulating service state change (critical, healthy, warning).
#### Verify Service Registration in Consul 
Open the [Consul Web UI](http://localhost:8500/ui), You should see `my-service` registered under services

#### Change Health Status Using Flask Health Service Endpoint:
##### Set to Warning:
```shell 
curl -X POST http://localhost:8080/set_health/warning
```
##### Set to Critical:
```shell 
curl -X POST http://localhost:8080/set_health/critical
```
##### Set to Passing (Healthy):
```shell 
curl -X POST http://localhost:8080/set_health/passing
```