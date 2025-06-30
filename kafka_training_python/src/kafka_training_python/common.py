import json
import random
from dataclasses import dataclass
from datetime import datetime

from pydantic_settings import BaseSettings

# Define the Avro schema for transaction messages based on CSV header
TRANSACTION_SCHEMA = """
{
    "type": "record",
    "name": "Transaction",
    "namespace": "de.kakadulabs.trainings.creditcardtransactions",
    "fields": [
        {"name": "timestamp", "type": "long", "logicalType": "timestamp-millis"},
        {"name": "cc_num", "type": "long"},
        {"name": "merchant", "type": "string"},
        {"name": "category", "type": "string"},
        {"name": "amt", "type": "double"},
        {"name": "first", "type": "string"},
        {"name": "last", "type": "string"},
        {"name": "country", "type": "string"}
    ]
}
"""

MERCHANTS = [
    "Amazon",
    "Apple",
    "Google",
    "Microsoft",
    "Facebook",
    "Twitter",
    "Instagram",
    "LinkedIn",
    "YouTube",
    "Netflix",
    "Otto",
    "Lidl",
    "Aldi",
    "Rewe",
    "Edeka",
    "Kaufland",
    "Lidl",
]
CATEGORIES = ["Groceries", "Restaurant", "Shopping", "Travel", "Entertainment", "Other"]
FIRST_NAMES = [
    "John",
    "Jane",
    "Jim",
    "Jill",
    "Jack",
    "Jill",
    "Jim",
    "Jane",
    "John",
    "Jim",
]
LAST_NAMES = [
    "Doe",
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
]
COUNTRIES = [
    "Germany",
    "France",
    "Italy",
    "Spain",
    "Portugal",
    "Greece",
    "Turkey",
    "Russia",
    "Ukraine",
    "Belarus",
]


@dataclass
class CreditCardTransaction:
    timestamp: datetime
    cc_num: int
    merchant: str
    category: str
    amt: float  # Should be decimal!
    first: str
    last: str
    country: str

    @classmethod
    def new_transaction(cls):
        return cls(
            timestamp=datetime.now(),
            cc_num=random.randint(1000000000000000, 9999999999999999),
            merchant=random.choice(MERCHANTS),
            category=random.choice(CATEGORIES),
            amt=random.randint(1, 100_000) / 100,  # 2 decimal places
            first=random.choice(FIRST_NAMES),
            last=random.choice(LAST_NAMES),
            country=random.choice(COUNTRIES),
        )

    def to_dict(self):
        return {
            "timestamp": int(self.timestamp.timestamp() * 1000),  # Convert to milliseconds
            "cc_num": self.cc_num,
            "merchant": self.merchant,
            "category": self.category,
            "amt": self.amt,
            "first": self.first,
            "last": self.last,
            "country": self.country,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


def register_avro_schema(schema_registry_client, schema):
    schema_registry_client.register_schema("credit-card-transactions-avro", schema)


def get_latest_avro_schema(schema_registry_client):
    return schema_registry_client.get_latest_version("credit-card-transactions-avro")


class Configuration(BaseSettings):
    kafka_bootstrap_servers: str
    schema_registry_url: str


configuration = Configuration()
