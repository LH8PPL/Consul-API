#!/bin/bash

cd $HOME

# Form Consul Cluster
ps -C consul
retval=$?
if [ $retval -eq 0 ]; then
  sudo killall consul
fi

sudo cp /vagrant/consul-config/consul-server.hcl /etc/consul.d/consul-server.hcl
sudo nohup consul agent --config-file /etc/consul.d/consul-server.hcl &>$HOME/consul.log &

# Wait for Consul to start
sleep 10

# Start the Flask service in the background
nohup python3 /vagrant/consul_service.py &> /vagrant/flask_service.log &

# Register the service with Consul
sudo consul services register /etc/consul.d/service.json
