from confluent_kafka import Consumer
from joblib import load
import mysql.connector
import json

def preprocess_transaction(transaction):
    """Convert a transaction into the required format for the model."""
    return [
        transaction["transaction_amount"],
        transaction["transaction_time"],
        transaction["customer_age"],
        transaction["location_risk_score"]
    ]

def consume_transactions():
    """Consume transactions from Kafka, predict fraud, and store results in MySQL."""
    # Load the trained fraud detection model
    model = load('fraud_detection_model.joblib')

    # Kafka consumer configuration
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',  # Kafka broker address
        'group.id': 'fraud-detection-group',   # Consumer group ID
        'auto.offset.reset': 'earliest'        # Start from the earliest message
    }
    consumer = Consumer(consumer_config)
    topic = 'transactions'

    # MySQL database connection
    db = mysql.connector.connect(
        host='localhost',
        user='abdullah',       # Replace with your MySQL username
        password='5545',   # Replace with your MySQL password
        database='fraud_database'    # Replace with your MySQL database name
    )
    cursor = db.cursor()

    # Subscribe to the Kafka topic
    consumer.subscribe([topic])

    print("Waiting for messages...")
    try:
        while True:
            msg = consumer.poll(1.0)  # Poll for new messages
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            # Deserialize the message value
            transaction = json.loads(msg.value().decode('utf-8'))

            # Preprocess and predict
            features = preprocess_transaction(transaction)
            prediction = model.predict([features])[0]  # Predict fraud or not
            is_fraud = bool(prediction)  # 1 -> True, 0 -> False

            # Print the prediction result
            print(f"Transaction: {transaction}")
            print(f"Fraud Detected: {is_fraud}")

            # Insert prediction result into the database
            try:
                cursor.execute("""
                    INSERT INTO fraud_predictions (transaction_amount, transaction_time, customer_age, location_risk_score, is_fraud)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    transaction["transaction_amount"],
                    transaction["transaction_time"],
                    transaction["customer_age"],
                    transaction["location_risk_score"],
                    is_fraud
                ))
                db.commit()
                print(f"Inserted into MySQL: {transaction} with is_fraud = {is_fraud}")
            except Exception as e:
                print(f"Error inserting into MySQL: {e}")

    except KeyboardInterrupt:
        print("Consumer interrupted by user.")
    finally:
        # Close the consumer and database connection
        consumer.close()
        cursor.close()
        db.close()

# Start the consumer
if __name__ == "__main__":
    consume_transactions()
