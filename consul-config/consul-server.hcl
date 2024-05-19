data_dir = "/opt/consul"

server           = true
bootstrap_expect = 1 
advertise_addr   = "{{ GetInterfaceIP `eth1` }}"
client_addr      = "0.0.0.0"

bind_addr        = "0.0.0.0"

connect {
  enabled = true
}
ui_config {
  enabled = true
}

ui               = true
datacenter       = "dc1"

telemetry {
  prometheus_retention_time = "30s"
}