from flask import Flask
import requests

app = Flask(__name__)

CONSUL_URL = 'http://host.docker.internal:8500/v1'

@app.get("/v1/api/consulCluster/status")
def get_status():
    response = requests.get(f'{CONSUL_URL}/agent/self')
    if response.status_code == 200:
        return {"status": 1, "message": "Consul server is running"}
    else:
        return {"status": 0, "message": "Consul server is down"}


@app.get("/v1/api/consulCluster/summary")
def get_summary():
    return {"registered_nodes": 5, "registered_services": 9, "leader": "1.2.3.4:8300", "cluster_protocol": 3}


@app.get("/v1/api/consulCluster/members")
def get_members():
    return {"registered_nodes": ["vag1.dc.com", "vag2.dc.com"]}


@app.get("/v1/api/consulCluster/systemInfo")
def get_systemInfo():
    return {"vCpus": "1", "MemoryGB": "1", "metric3": "1"}