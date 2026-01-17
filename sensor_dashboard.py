import os, json, time
import matplotlib.pyplot as plt
from collections import defaultdict

CURATED = r"C:\factory\curated\sensor"

plt.ion()
fig, ax = plt.subplots()

while True:
    data = defaultdict(list)

    for f in os.listdir(CURATED):
        if not f.endswith(".json"):
            continue

        with open(os.path.join(CURATED, f)) as fh:
            rows = json.load(fh)

        for r in rows:
            data[r["sensor_id"]].append(r["avg_value"])

    ax.clear()
    for sid, vals in data.items():
        ax.plot(vals, label=sid)

    ax.set_title("Sensor Average Value")
    ax.set_xlabel("time bucket")
    ax.set_ylabel("avg_value")
    ax.legend()

    plt.pause(5)
