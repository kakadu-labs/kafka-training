import logging
import sys
from datetime import datetime
from decimal import Decimal as D

from confluent_kafka import Consumer
from pydantic import BaseModel

from kafka_training_python.common import configuration

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


class CreditCardTransaction(BaseModel):
    timestamp: datetime
    cc_num: int
    merchant: str
    category: str
    amt: D
    first: str
    last: str
    country: str
    timestamp: int


def main():
    c = Consumer(
        {
            "bootstrap.servers": configuration.kafka_bootstrap_servers,
            "group.id": "simple-json-consumer",
            "auto.offset.reset": "earliest",
        }
    )
    c.subscribe(["credit-card-transactions-json"])

    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logger.error(msg.error())
            continue
        message = msg.value()
        transaction = CreditCardTransaction.model_validate_json(message)
        logger.info(
            f"Transaction: {transaction}",
            extra={"Message size in bytes:": sys.getsizeof(msg.value())},
        )
        print(transaction)


if __name__ == "__main__":
    main()
