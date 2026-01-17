import os, json, time
from datetime import datetime

RAW = r"C:\factory\raw\sensor"
STAGING = r"C:\factory\staging\sensor"
SEEN = set()

def clean(record):
    record["value"] = float(record["value"])
    record["timestamp"] = datetime.fromisoformat(record["timestamp"]).isoformat()
    return record

while True:
    for root, dirs, files in os.walk(RAW):
        for f in files:
            if not f.endswith(".json"):
                continue

            path = os.path.join(root,f)
            if path in SEEN:
                continue

            with open(path) as fh:
                record = json.load(fh)

            record = clean(record)

            rel = os.path.relpath(root, RAW)
            outdir = os.path.join(STAGING, rel)
            os.makedirs(outdir, exist_ok=True)

            outpath = os.path.join(outdir, f)
            with open(outpath,"w") as out:
                json.dump(record,out)

            SEEN.add(path)
            print("cleaned", outpath)

    time.sleep(5)
