from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# Define the training data
X_train = [
    [100, 14, 30, 20],  # Legitimate
    [1000, 2, 45, 80],  # Fraud
    [50, 10, 25, 10],   # Legitimate
    [500, 23, 55, 60],  # Fraud
    [75, 16, 40, 15],   # Legitimate
    [1200, 1, 35, 85],  # Fraud
    [90, 20, 50, 25],   # Legitimate
    [2000, 3, 60, 95]   # Fraud
]
y_train = [0, 1, 0, 1, 0, 1, 0, 1]

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
dump(model, 'fraud_detection_model.joblib')
print("Model trained and saved as 'fraud_detection_model.joblib'.")
