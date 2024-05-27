# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "bento/ubuntu-24.04"
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = true
  
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    # Customize the amount of CPU on the VM:
    vb.cpus = "1"
  end

  # Server (consul)
  config.vm.define "consul01" do |n|
    n.vm.provision "shell", path: "node-install.sh"
    n.vm.provision "shell", path: "launch-server.sh", run: 'always'
    # Forward ports for Consul UI and agent
    n.vm.network "forwarded_port", guest: 8500, host: 8500
    n.vm.network "forwarded_port", guest: 8080, host: 8080
    n.vm.hostname = "consul01"
    n.vm.network "private_network", ip: "172.16.1.101"
  end
end
