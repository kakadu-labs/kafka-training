import sys

from confluent_kafka import Consumer

from kafka_training_python.common import configuration


def main():
    c = Consumer(
        {
            "bootstrap.servers": configuration.kafka_bootstrap_servers,
            "group.id": "get-payload-size",
            "auto.offset.reset": "earliest",
        }
    )
    c.subscribe(["credit-card-transactions-avro"])

    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue
        print(f"Message size in bytes: {sys.getsizeof(msg.value())}")


if __name__ == "__main__":
    main()
