import os, json, time, csv
from datetime import datetime

CURATED = r"C:\factory\curated\sensor"
WAREHOUSE = r"C:\factory\warehouse"
SEEN = set()

def save_partitioned(row):
    sensor_id = row[0]
    now = datetime.now()

    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    base_path = os.path.join(WAREHOUSE, sensor_id, "csv", year, month)
    os.makedirs(base_path, exist_ok=True)

    file_path = os.path.join(base_path, f"{day}.csv")

    header = ["sensor_id", "minute", "avg_value", "count"]
    write_header = not os.path.exists(file_path)

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow(header)

        writer.writerow(row)

    print("Saved ->", file_path)

while True:
    for f in os.listdir(CURATED):
        if not f.endswith(".json"):
            continue

        path = os.path.join(CURATED, f)
        if path in SEEN:
            continue

        with open(path) as fh:
            rows = json.load(fh)

        for r in rows:
            save_partitioned([r["sensor_id"], r["minute"], r["avg_value"], r["count"]])

        SEEN.add(path)
        print("loaded", path)

    time.sleep(10)
