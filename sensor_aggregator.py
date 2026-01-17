import os, json, time
from collections import defaultdict
from datetime import datetime

STAGING = r"C:\factory\staging\sensor"
CURATED = r"C:\factory\curated\sensor"
SEEN = set()

while True:
    bucket = defaultdict(list)

    for root, dirs, files in os.walk(STAGING):
        for f in files:
            if not f.endswith(".json"):
                continue

            path = os.path.join(root,f)
            if path in SEEN:
                continue

            with open(path) as fh:
                r = json.load(fh)

            ts = datetime.fromisoformat(r["timestamp"])
            key = (r["sensor_id"], ts.strftime("%Y-%m-%d %H:%M"))
            bucket[key].append(r["value"])

            SEEN.add(path)

    if bucket:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(CURATED, exist_ok=True)
        out = os.path.join(CURATED, f"agg_{now}.json")

        rows = []
        for (sid, minute), vals in bucket.items():
            rows.append({
                "sensor_id": sid,
                "minute": minute,
                "avg_value": round(sum(vals)/len(vals),2),
                "count": len(vals)
            })

        with open(out,"w") as f:
            json.dump(rows,f,indent=2)

        print("aggregated", out)

    time.sleep(30)
