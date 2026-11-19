from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model.pkl")

correct = 0
total = 0

@app.get("/")
def home():
    return {"message": "Intrusion Detection System Running"}

@app.post("/predict")
def predict(packet_size: float, rssi: float):
    global correct, total

    data = [[packet_size, rssi]]
    prediction = model.predict(data)[0]

    # Better simulated ground truth
    true_label = -1 if (packet_size > 200 and rssi < -80) else 1

    if prediction == true_label:
        correct += 1

    total += 1

    accuracy = correct / total if total > 0 else 0

    return {
        "status": "ANOMALY 🚨" if prediction == -1 else "NORMAL ✅",
        "accuracy": round(accuracy, 2)
    }
# python -m uvicorn app:app --reload
