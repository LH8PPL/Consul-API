#!/bin/bash
# Update the package list and install prerequisites
sudo apt-get update -y
sudo apt-get install unzip curl vim jq python3-pip -y

# make an archive folder to move old binaries into
if [ ! -d /tmp/archive ]; then
  sudo mkdir /tmp/archive/
fi

echo "Consul Install Beginning..."
# Download and install Consul
CONSUL_VERSION=$(curl -s https://checkpoint-api.hashicorp.com/v1/check/consul | jq -r ".current_version")
sudo curl -sSL https://releases.hashicorp.com/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip > /tmp/consul.zip
if [ ! -d consul ]; then
  sudo unzip /tmp/consul.zip
fi
if [ ! -f /usr/bin/consul ]; then
  sudo install consul /usr/bin/consul
fi
if [ -f /tmp/archive/consul ]; then
  sudo rm /tmp/archive/consul
fi
# Create Consul directories
sudo mv consul /tmp/archive/consul
sudo mkdir -p /etc/consul.d
sudo chmod a+w /etc/consul.d

# Create Consul configuration
sudo cp /vagrant/consul-config/consul-server.hcl /etc/consul.d/
sudo cp /vagrant/consul-config/consul-client.hcl /etc/consul.d/

# Move the service definition file to Consul configuration directory
sudo cp /vagrant/service.json /etc/consul.d/

# Install Flask using apt
sudo apt-get install -y python3-flask

