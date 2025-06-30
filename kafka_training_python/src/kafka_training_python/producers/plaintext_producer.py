import logging
import time

from confluent_kafka import Producer

from kafka_training_python.common import configuration

logger = logging.getLogger(__name__)


def on_delivery(err, msg):
    if err:
        logger.error(f"Delivery failed for message: {msg.value()}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


def main():
    p = Producer({"bootstrap.servers": configuration.kafka_bootstrap_servers})

    try:
        while True:
            # API DOCS here: https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#pythonclient-producer
            p.produce(topic="test", key="key", value="Hello, World!", on_delivery=on_delivery)
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt")
        p.flush()
    except SystemExit:
        p.flush()
    except Exception as e:
        logger.error(f"Error: {e}")
        p.flush()
    finally:
        p.flush()


if __name__ == "__main__":
    main()
