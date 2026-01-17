import os, json, random, time
from datetime import datetime

BASE = r"C:\factory\raw\sensor"

sensors = [
    ("S-01","temperature","C",60,95),
    ("S-02","vibration","hz",5,40),
    ("S-03","speed","rpm",800,2000)
]

while True:
    now = datetime.now()
    path = os.path.join(BASE, now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"), now.strftime("%H"))
    os.makedirs(path, exist_ok=True)

    sensor_id, t, unit, lo, hi = random.choice(sensors)
    record = {
        "sensor_id": sensor_id,
        "type": t,
        "value": round(random.uniform(lo,hi),2),
        "unit": unit,
        "timestamp": now.isoformat()
    }

    fname = f"{now.strftime('%H%M%S')}_{sensor_id}.json"
    with open(os.path.join(path,fname),"w") as f:
        json.dump(record,f)

    print("emitted", record)
    time.sleep(10)
