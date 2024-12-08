# Real-time_Fraud_Detection_Using_Kafka
A real-time fraud detection system using Kafka for data streaming, a machine learning model ( Random Forest ) for predictions, and MySQL for storage.

This project demonstrates a real-time fraud detection system using Kafka for data streaming, a machine learning model for fraud prediction, and MySQL for data storage. Follow this step-by-step guide to deploy and test the system on your Linux system.

## Prerequisites

Ensure the following are installed on your system:

- Python 3.x
- Kafka (Apache Kafka)
- MySQL Database Server
- Confluent Kafka Python library
- scikit-learn (or other required libraries)

## Step-by-Step Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Abdullah-Abuslama/Real-time_Fraud_Detection_Using_Kafka.git
cd Real-time_Fraud_Detection_Using_Kafka
```

## 2. Set Up the MySQL Database and Table

### Log in to MySQL:

```bash
mysql -u root -p
```

### Create the database and table:

```sql
CREATE DATABASE fraud_database;

USE fraud_database;

CREATE TABLE fraud_predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_amount DECIMAL(10, 2) NOT NULL,
    transaction_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    customer_age INT NOT NULL,
    location_risk_score INT NOT NULL,
    is_fraud BOOLEAN DEFAULT FALSE
);

```
### Create a user with the necessary privileges:


```sql
CREATE USER 'fraud_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON fraud_database.* TO 'fraud_user'@'localhost';
FLUSH PRIVILEGES;

```

## 3. Set Up Kafka

### Start ZooKeeper (if needed):

```bash
./bin/zookeeper-server-start.sh config/zookeeper.properties

```

### Start Kafka:

```bash
./bin/kafka-server-start.sh config/server.properties

```

### Create a Kafka topic:

```bash
./bin/kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

```


## 4. Run the Kafka Producer

### Ensure you are in the project directory and run:

```bash
python kafka_producer.py
```

## 5. Run the Kafka Consumer

### Start the consumer script to process data from Kafka and store predictions in the MySQL database:

```bash
python kafka_consumer.py
```

## 6. Verify Data in MySQL

### Log in to MySQL:

```bash
mysql -u fraud_user -p
```

### Check the fraud_predictions table:
```sql
USE fraud_database;
SELECT * FROM fraud_predictions;
```
You should see the stored transaction details along with the prediction (the is_fraud column indicating if the transaction is predicted as fraudulent).


## Explanation of the Code

### kafka_producer.py
Generates simulated transaction data and sends it to the Kafka `transactions` topic.

### kafka_consumer.py
Consumes data from the Kafka `transactions` topic, processes it using a trained machine learning model (`fraud_detection_model.joblib`), and stores the prediction results in the `fraud_predictions` table of the `fraud_database`.

### Database Table (`fraud_predictions`)
- **prediction_id**: Auto-incremented primary key.
- **transaction_amount**: The amount of the transaction.
- **transaction_time**: The timestamp when the transaction was processed.
- **customer_age**: Age of the customer.
- **location_risk_score**: Risk score associated with the transaction location.
- **is_fraud**: Indicates whether the transaction was flagged as fraudulent (TRUE) or not (FALSE).

## Troubleshooting
- Ensure Kafka and Zookeeper are running before executing the producer and consumer scripts.
- Verify MySQL user credentials and permissions if there are any access issues.

