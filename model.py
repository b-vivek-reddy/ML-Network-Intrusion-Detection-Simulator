import pandas as pd
from sklearn.ensemble import IsolationForest

# Load data
data = pd.read_csv("network_data.csv")

# Train model
model = IsolationForest(contamination=0.2)
model.fit(data)

# Save model
import joblib
joblib.dump(model, "model.pkl")

print("Model trained!")