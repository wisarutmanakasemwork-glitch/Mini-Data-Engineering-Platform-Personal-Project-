import os, json, time
from datetime import datetime

STAGING = r"C:\factory\staging\sensor"
ALERT = r"C:\factory\alerts"
SEEN = set()

RULES = {
    "temperature": lambda v: v > 90,
    "vibration": lambda v: v > 30,
    "speed": lambda v: v > 1800
}

while True:
    for root, dirs, files in os.walk(STAGING):
        for f in files:
            if not f.endswith(".json"):
                continue

            path = os.path.join(root, f)
            if path in SEEN:
                continue

            with open(path) as fh:
                r = json.load(fh)

            sensor_type = r["type"]
            value = r["value"]

            if sensor_type in RULES and RULES[sensor_type](value):
                os.makedirs(ALERT, exist_ok=True)

                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                out = os.path.join(ALERT, f"alert_{now}_{r['sensor_id']}.json")

                with open(out, "w") as f:
                    json.dump(r, f, indent=2)

                print("🚨 ALERT:", r)

            SEEN.add(path)

    time.sleep(3)
