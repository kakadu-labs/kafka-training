import logging
import time

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import Schema, SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

from kafka_training_python.common import (
    TRANSACTION_SCHEMA,
    CreditCardTransaction,
    configuration,
    register_avro_schema,
)

logger = logging.getLogger(__name__)


def avro_producer_factory(schema_str):
    """Create a producer with Avro serialization using schema registry."""

    # Schema Registry client configuration
    schema_registry_conf = {"url": configuration.schema_registry_url}

    # Create schema registry client
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    schema = Schema(TRANSACTION_SCHEMA, "AVRO")
    # Create Avro serializer for values
    avro_serializer = AvroSerializer(schema_registry_client, schema_str, conf={"auto.register.schemas": True})

    # Create string serializer for keys
    string_serializer = StringSerializer("utf_8")

    # Producer configuration
    producer_conf = {
        "bootstrap.servers": configuration.kafka_bootstrap_servers,
        "key.serializer": string_serializer,
        "value.serializer": avro_serializer,
        "compression.type": "snappy",
    }

    return SerializingProducer(producer_conf)


def main():
    schema_registry_conf = {"url": configuration.schema_registry_url}

    # Create schema registry client
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    schema = Schema(TRANSACTION_SCHEMA, "AVRO")
    register_avro_schema(schema_registry_client, schema)

    producer = avro_producer_factory(schema.schema_str)
    try:
        transaction_id = 1
        while True:
            new_transaction = CreditCardTransaction.new_transaction()
            # Convert to dictionary for Avro serialization
            transaction_dict = new_transaction.to_dict()
            # Produce the message
            producer.produce(
                topic="credit-card-transactions-avro",
                key=new_transaction.last,
                value=new_transaction.to_dict(),
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
