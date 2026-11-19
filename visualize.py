import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("network_data.csv")

plt.scatter(data["packet_size"], data["rssi"])
plt.xlabel("Packet Size")
plt.ylabel("RSSI")
plt.title("Network Traffic Visualization")

plt.show()