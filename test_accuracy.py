import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load model
model = joblib.load("model.pkl")

# Create labeled dataset
normal = pd.DataFrame({
    "packet_size": np.random.normal(100, 10, 200),
    "rssi": np.random.normal(-60, 5, 200),
    "label": 1   # normal
})

anomaly = pd.DataFrame({
    "packet_size": np.random.normal(300, 50, 50),
    "rssi": np.random.normal(-90, 10, 50),
    "label": -1  # anomaly
})

data = pd.concat([normal, anomaly])

X = data[["packet_size", "rssi"]]
y_true = data["label"]

# Predict
y_pred = model.predict(X)

# Accuracy
accuracy = accuracy_score(y_true, y_pred)

print("Accuracy:", accuracy)

# Detailed report
print("\nClassification Report:\n")
print(classification_report(y_true, y_pred))

# Confusion matrix
print("\nConfusion Matrix:\n")
print(confusion_matrix(y_true, y_pred))