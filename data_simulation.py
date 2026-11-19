import pandas as pd
import numpy as np

# Normal traffic
normal = pd.DataFrame({
    "packet_size": np.random.normal(100, 10, 200),
    "rssi": np.random.normal(-60, 5, 200)
})

# Anomalous traffic
anomaly = pd.DataFrame({
    "packet_size": np.random.normal(300, 50, 50),
    "rssi": np.random.normal(-90, 10, 50)
})

data = pd.concat([normal, anomaly])
data.to_csv("network_data.csv", index=False)

print("Dataset created!")