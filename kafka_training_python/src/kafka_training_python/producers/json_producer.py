import logging
import time

from confluent_kafka import Producer, SerializingProducer
from confluent_kafka.serialization import StringSerializer

from kafka_training_python.common import (
    TRANSACTION_SCHEMA,
    CreditCardTransaction,
    configuration,
)

logger = logging.getLogger(__name__)


def avro_producer_factory(schema_str):
    """Create a producer with Avro serialization using schema registry."""

    # Create Avro serializer for values

    # Create string serializer for keys
    string_serializer = StringSerializer("utf_8")

    # Producer configuration
    producer_conf = {
        "bootstrap.servers": configuration.kafka_bootstrap_servers,
        "key.serializer": string_serializer,
        "value.serializer": string_serializer,
    }

    return SerializingProducer(producer_conf)


def main():
    schema_registry_conf = {"url": configuration.schema_registry_url}
    producer = Producer({"bootstrap.servers": configuration.kafka_bootstrap_servers})
    # Create schema registry client

    try:
        while True:
            new_transaction = CreditCardTransaction.new_transaction()

            # Produce the message
            producer.produce(
                topic="credit-card-transactions-json",
                key=new_transaction.last,
                value=new_transaction.to_json(),
            )
            logger.info(f"Produced transaction: {new_transaction}")
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt")
        producer.flush()
    except SystemExit:
        producer.flush()
    except Exception as e:
        logger.error(f"Error: {e}")
        producer.flush()
    finally:
        producer.flush()


if __name__ == "__main__":
    main()
