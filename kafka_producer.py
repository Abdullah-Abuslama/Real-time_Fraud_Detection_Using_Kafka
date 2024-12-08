from confluent_kafka import Producer
import random
import json

def generate_transaction():
    """Simulate generating a transaction."""
    transaction = {
        "transaction_amount": random.randint(10, 5000),  # Amount in USD
        "transaction_time": random.randint(0, 23),      # Hour of the day
        "customer_age": random.randint(18, 75),         # Customer age
        "location_risk_score": random.randint(1, 100)   # Risk score (1-100)
    }
    return transaction

def delivery_report(err, msg):
    """Callback for delivery reports."""
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Configure producer
producer_config = {
    'bootstrap.servers': 'localhost:9092'  # Kafka broker address
}
producer = Producer(producer_config)

# Produce transactions
topic = 'transactions'
for _ in range(5):
    transaction = generate_transaction()
    producer.produce(
        topic=topic,
        value=json.dumps(transaction),
        callback=delivery_report
    )
    producer.flush()
