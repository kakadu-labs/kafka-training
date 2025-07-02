resource "kafka_topic" "tf_created_test" {
  name               = "tf_created_test"
  replication_factor = 2
  partitions         = 100

  config = {
    "segment.ms"     = "20000"
    "cleanup.policy" = "compact"
  }
}


resource "kafka_topic" "credit_card_transactions_avro" {
  name               = "credit-card-transactions-avro"
  replication_factor = 3
  partitions         = 100

  config = {
    "retention.bytes" = 512*1000000 # 512 MB
  }
}


resource "kafka_topic" "credit_card_transactions_json" {
  name               = "credit-card-transactions-json"
  replication_factor = 3
  partitions         = 10

  config = {
    "min.insync.replicas"     = "2"
  }
}
