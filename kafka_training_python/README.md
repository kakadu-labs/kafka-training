# Simple Kafka Producers

A collection of simple Kafka producer examples for learning and development purposes.

## Features

- **Plaintext Producer**: A basic producer that sends "Hello, World!" messages to a Kafka topic
- **Modular Design**: Easy to extend with new producer types
- **CLI Interface**: Simple command-line interface for running different producers
- **Configurable Logging**: Adjustable log levels for debugging

## Installation

This project uses `uv` for dependency management. To install:

```bash
# Install dependencies
uv sync

# Install the package in development mode
uv pip install -e .
```

## Usage

### Running the Entrypoint

The main entrypoint provides a command-line interface for running different types of producers:

```bash
# Run the default plaintext producer
python -m src

# Run with explicit producer type
python -m src --producer plaintext

# Run with debug logging
python -m src --producer plaintext --log-level DEBUG

# Show help
python -m src --help
```

### After Installation

Once installed, you can also run the producers using the installed script:

```bash
# Run the default producer
simple_producers

# Run with options
simple_producers --producer plaintext --log-level DEBUG
```

### Direct Module Execution

You can also run individual producers directly:

```bash
# Run the plaintext producer directly
python src/plaintext_producer/plaintext_producer.py
```

## Configuration

### Kafka Configuration

The Kafka client is configured in `src/plaintext_producer/kafka_client.py`:

```python
from confluent_kafka import Producer

p = Producer({"bootstrap.servers": "localhost:9092, localhost:9093, localhost:9094"})
```

Make sure your Kafka cluster is running on the configured servers before running the producers.

### Topic Configuration

The plaintext producer sends messages to the `test` topic by default. You can modify this in the producer code.

## Development

### Project Structure

```
simple_producers/
├── src/
│   ├── __main__.py              # Main entrypoint
│   └── plaintext_producer/
│       ├── __init__.py
│       ├── kafka_client.py      # Kafka client configuration
│       └── plaintext_producer.py # Plaintext producer implementation
├── pyproject.toml               # Project configuration
├── uv.lock                      # Dependency lock file
└── README.md                    # This file
```

### Adding New Producers

To add a new producer type:

1. Create a new module in `src/` (e.g., `src/json_producer/`)
2. Implement your producer logic
3. Add the producer type to the choices in `src/__main__.py`
4. Add a corresponding run function in `src/__main__.py`

### Code Quality

This project uses `ruff` for linting and formatting:

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Fix linting issues
uv run ruff check --fix .
```

## Requirements

- Python 3.12+
- Kafka cluster running on localhost:9092, localhost:9093, localhost:9094
- Dependencies managed by `uv`

## License

[Add your license information here]
