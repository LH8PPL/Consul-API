from flask import Flask
import requests
import os
import psutil # i would have used the prometheus client and/or prometheus flask for scraping or exporting metrics to a monitoring system 

app = Flask(__name__)

CONSUL_URL = 'http://host.docker.internal:8500/v1'

# https://developer.hashicorp.com/consul/api-docs/status
# used /status/leader instead of /agent/self, looks like a better check, /status/peers could do the job too
@app.get("/v1/api/consulCluster/status")
def get_status():
    try:
        response = requests.get(f'{CONSUL_URL}/status/leader')
        if response.status_code == 200:
            return {"status": 1, "message": "Consul server is running"}
        else:
            return {"status": 0, "message": "Consul server is down"}, response.status_code # If the status code is not 200, it returns that the Consul server is down, along with the actual status code from the response
    except requests.exceptions.RequestException as e: #All exceptions that Requests explicitly raises inherit from
        return {"status": 0, "message": str(e)}, 500
    
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
    response = requests.get(f'{CONSUL_URL}/catalog/nodes')
    members = [member['Node'] for member in response.json()]
    return {"registered_nodes": members}


@app.get("/v1/api/consulCluster/systemInfo")
def get_systemInfo():
    # System information
    system_info = {
        "vCpus": os.cpu_count(),
        "MemoryGB": round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024.**3), 2),
        "HostName": os.uname()[1],
        "OS": os.uname()[0],
        "KernelVersion": os.uname()[2],
        "Architecture": os.uname()[4],
        "CPU_Usage_Percentage": psutil.cpu_percent(interval=1),
        "Memory_Usage_Percentage": psutil.virtual_memory().percent,
        "Disk_Usage_Percentage": psutil.disk_usage('/').percent,
        "Network_Bytes_Sent": psutil.net_io_counters().bytes_sent,
        "Network_Bytes_Received": psutil.net_io_counters().bytes_recv,
        "Load_Average_1min": os.getloadavg()[0],
        "Load_Average_5min": os.getloadavg()[1],
        "Load_Average_15min": os.getloadavg()[2]
    }
    return system_info
    #return {"vCpus": "1", "MemoryGB": "1", "metric3": "1"}