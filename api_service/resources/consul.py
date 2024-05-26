from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
import os
import psutil

CONSUL_URL = 'http://host.docker.internal:8500/v1'

blp = Blueprint("consulCluster", __name__, description="Operations on consulCluster")

@blp.route("/v1/api/consulCluster/status")
class Status(MethodView):
    def get(self):
        try:
            response = requests.get(f'{CONSUL_URL}/status/leader')
            if response.status_code == 200:
                return {"status": 1, "message": "Consul server is running"}
            else:
                return {"status": 0, "message": "Consul server is down"}, response.status_code # If the status code is not 200, it returns that the Consul server is down, along with the actual status code from the response
        except requests.exceptions.RequestException as e: #All exceptions that Requests explicitly raises inherit from
            return {"status": 0, "message": str(e)}, 500

@blp.route("/v1/api/consulCluster/summary")
class Summary(MethodView):
    def get(self):
        try:
            nodes_response = requests.get(f'{CONSUL_URL}/catalog/nodes')
            services_response = requests.get(f'{CONSUL_URL}/catalog/services')
            status_response = requests.get(f'{CONSUL_URL}/status/leader')
            agent_self = requests.get(f'{CONSUL_URL}/agent/self')
            if (
                nodes_response.status_code == 200 
                and services_response.status_code == 200 
                and status_response.status_code == 200
                ):
                registered_services = len(services_response.json())
                registered_nodes = len(nodes_response.json())
                leader = status_response.text.strip('"')
                protocol_version = agent_self.json()['Stats']['raft']['protocol_version']
                return {"registered_nodes": registered_nodes, "registered_services": registered_services, "leader": leader, "cluster_protocol": protocol_version}
            else:
                abort(500, message="Failed to retrieve summary")
        except requests.exceptions.RequestException as e:
            abort(500, message=str(e))

@blp.route("/v1/api/consulCluster/members")
class Members(MethodView):
    def get(self):
        try:
            response = requests.get(f'{CONSUL_URL}/catalog/nodes')
            if response.status_code == 200:
                members = [member['Node'] for member in response.json()]
                return {"registered_nodes": members}
            else:
                abort(response.status_code, message="Failed to retrieve members")
        except requests.exceptions.RequestException as e:
            abort(500, message=str(e))

@blp.route("/v1/api/consulCluster/systemInfo")
class SystemInfo(MethodView):
    def get(self):
        try:
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
        except Exception as e:
            abort(500, message=str(e))