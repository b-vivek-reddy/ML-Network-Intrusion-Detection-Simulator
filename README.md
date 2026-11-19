# ML-Network-Intrusion-Detection-Simulator

A small machine learning project that detects anomalous network traffic using an **Isolation Forest** model, serves predictions through a **FastAPI** backend, and visualizes everything on a **real-time web dashboard**.

The system looks at two features of each network packet, **packet size** and **RSSI** (signal strength in dBm), and flags unusual combinations as intrusions.

---

## Features

- Unsupervised anomaly detection with scikit-learn's `IsolationForest`
- Synthetic dataset generator for normal and anomalous traffic
- REST API (`/predict`) built with FastAPI
- Live dashboard with:
  - Status card (NORMAL / ALERT)
  - Running accuracy and threat counter
  - Real-time packet size chart (Chart.js) with anomalies highlighted
  - Live alert feed with an audio beep on detection
- Standalone evaluation script with accuracy, classification report and confusion matrix
- Scatter plot script to visualize the dataset

---

## Project Structure

```
MLProject/
├── app.py               # FastAPI backend serving the model
├── data_simulation.py   # Generates network_data.csv (normal + anomalous traffic)
├── model.py             # Trains the Isolation Forest and saves model.pkl
├── test_accuracy.py     # Evaluates the model on a freshly generated labeled set
├── visualize.py         # Scatter plot of packet size vs RSSI
├── network_data.csv     # Generated dataset (250 samples)
├── model.pkl            # Trained model
└── dashboard/
    ├── index.html       # Dashboard UI
    └── script.js        # Polling logic, chart and alert handling
```

---

## How It Works

1. **Data simulation** (`data_simulation.py`) creates 250 samples:

   | Class   | Samples | Packet size (mean ± std) | RSSI (mean ± std) |
   | ------- | ------- | ------------------------ | ----------------- |
   | Normal  | 200     | 100 ± 10                 | -60 ± 5 dBm       |
   | Anomaly | 50      | 300 ± 50                 | -90 ± 10 dBm      |

2. **Training** (`model.py`) fits an `IsolationForest(contamination=0.2)` on the dataset and saves it with `joblib`.
3. **Serving** (`app.py`) loads `model.pkl` and exposes a `/predict` endpoint. The model returns `1` for normal and `-1` for anomaly.
4. **Dashboard** (`dashboard/`) sends a new reading to the API every 2 seconds and updates the UI with the result.

---

## Getting Started

### Prerequisites

- Python 3.9+
- A modern web browser

### 1. Install dependencies

```bash
pip install fastapi uvicorn scikit-learn pandas numpy joblib matplotlib
```

### 2. (Optional) Regenerate the data and retrain the model

A dataset and a trained model are already included. To rebuild them:

```bash
python data_simulation.py
python model.py
```

> **Note:** `model.pkl` should be loaded with the same scikit-learn version it was trained with. If you see a version warning or error, just re-run `python model.py`.

### 3. Start the API

Run this from the project root (the app loads `model.pkl` using a relative path):

```bash
python -m uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 4. Open the dashboard

Open `dashboard/index.html` in your browser. It will start polling the API automatically.

---

## API Reference

### `GET /`

Health check.

```json
{ "message": "IDS Running" }
```

### `POST /predict`

Classifies a single packet reading.

**Query parameters**

| Name          | Type  | Description                   |
| ------------- | ----- | ----------------------------- |
| `packet_size` | float | Size of the packet            |
| `rssi`        | float | Received signal strength (dBm) |

**Example**

```bash
curl -X POST "http://127.0.0.1:8000/predict?packet_size=320&rssi=-92"
```

**Response**

```json
{
  "status": "ANOMALY 🚨",
  "accuracy": 0.87
}
```

`status` is either `"NORMAL ✅"` or `"ANOMALY 🚨"`. `accuracy` is the running accuracy since the server started.

---

## Evaluating the Model

```bash
python test_accuracy.py
```

This generates a fresh labeled dataset (200 normal + 50 anomalous samples), runs the model on it, and prints the accuracy, a classification report and a confusion matrix.

To view the dataset as a scatter plot:

```bash
python visualize.py
```

---

## Important Notes

- **Simulated traffic:** the dashboard generates random packet and RSSI values in the browser (about 20% anomalous). It does not capture real network traffic.
- **Running accuracy is approximate:** because the dashboard data is simulated, `app.py` uses a rule-based ground truth with some randomness to compute the live accuracy. For a proper measurement, use `test_accuracy.py`.
- **Internet access for the dashboard:** Chart.js is loaded from a CDN and the alert sound from an external URL, so the dashboard needs an internet connection for those.
- **CORS is open** (`allow_origins=["*"]`) for local development convenience. Restrict it before any real deployment.

---

## Tech Stack

- **ML:** scikit-learn (Isolation Forest), pandas, NumPy, joblib
- **Backend:** FastAPI, Uvicorn
- **Frontend:** HTML, CSS, vanilla JavaScript, Chart.js
- **Visualization:** Matplotlib

---

## Possible Improvements

- Feed the model with real captured network data
- Add more features (protocol, inter-arrival time, packet count)
- Persist alerts to a database and add a history view
- Replace polling with WebSockets for true streaming
- Containerize the project with Docker

---

## License

Add your preferred license here (e.g., MIT).
