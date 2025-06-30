resource "kafka_topic" "tf_created_test" {
  name               = "tf_created_test"
  replication_factor = 2
  partitions         = 5

  config = {
    "segment.ms"     = "20000"
    "cleanup.policy" = "compact"
  }
}
