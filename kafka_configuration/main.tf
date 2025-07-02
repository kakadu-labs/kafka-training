terraform {
  required_providers {
    kafka = {
      source = "Mongey/kafka"
    }
  }
}

provider "kafka" {
  bootstrap_servers = ["116.203.255.71:9092", "116.203.255.71:9093", "116.203.255.71:9094"]
  tls_enabled = false
}
