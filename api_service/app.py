from flask import Flask
import requests

app = Flask(__name__)

CONSUL_URL = 'http://host.docker.internal:8500/v1'

# https://developer.hashicorp.com/consul/api-docs/status
# used /status/leader instead of /agent/self, looks like a better check, /status/peers could do the job too
@app.get("/v1/api/consulCluster/status")
def get_status():
    response = requests.get(f'{CONSUL_URL}/agent/self')
    if response.status_code == 200:
        return {"status": 1, "message": "Consul server is running"}
    else:
        return {"status": 0, "message": "Consul server is down"}

# https://developer.hashicorp.com/consul/api-docs/catalog
# 
@app.get("/v1/api/consulCluster/summary") 
def get_summary():
    nodes_response = requests.get(f'{CONSUL_URL}/catalog/nodes')
    services_response = requests.get(f'{CONSUL_URL}/catalog/services')
    status_response = requests.get(f'{CONSUL_URL}/status/leader')
    agent_self = requests.get(f'{CONSUL_URL}/agent/self')
    
    registered_services = len(services_response.json())
    registered_nodes = len(nodes_response.json())
    leader = status_response.text.strip('"')
    protocol_version = agent_self.json()['Stats']['raft']['protocol_version']

    return {"registered_nodes": registered_nodes, "registered_services": registered_services, "leader": leader, "cluster_protocol": protocol_version}


@app.get("/v1/api/consulCluster/members")
def get_members():
    return {"registered_nodes": ["vag1.dc.com", "vag2.dc.com"]}


@app.get("/v1/api/consulCluster/systemInfo")
def get_systemInfo():
    return {"vCpus": "1", "MemoryGB": "1", "metric3": "1"}