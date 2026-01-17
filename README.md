# Mini-Data-Engineering-Personal-Project-
โปรเจคนี้เป็นการจำลองโรงงานโดยมี sensor คอยตรวจจับข้อมูลจำวพวก temperature vibration speed และส่งข้อมูลเข้ามาตลอดเวลา 
โดยไฟล์ `sensor_generator.py` จะเป็นตัวสร้างข้อมูลที่ได้ออกมาเรื่อย ๆ ไปเก็บใน raw โฟรเดอร์ เราจะต้องจัดการกับไฟล์ที่มาเรื่อย ๆ นี่ให้ได้

`sensor_cleaner.py` จะทำหน้าที่ clean ข้อมูลในโฟรเดอร์ raw และส่งไปที่โฟรเดอร์ staging 
Sensor → RAW → Cleaning Worker → STAGING 

`sensor_aggregator.py` จะทำหน้าที่ read ข้อมูลในโฟรเดอร์ staging แล้วรวมตาม sensor_id จากนั้นส่งไปโฟรเดอร์ curated 
RAW → STAGING → CURATED 

จากข้อมูลที่ได้มาจึงได้ทำระบบป้องกันอันตราย โดยกำหนด 
temp > 90 = อันตราย 
vibration > 30 = อันตราย 
speed > 1800 = อันตราย 

`sensor_alert.py` ก็จะขึ้นบอกว่าเวลาไหน sensor ตัวไหนเกินที่กำหนดจะส่งไฟล์ไปโฟรเดอร์ Alert 
`sensor_dashboard.py` เอาไว้ดูกราฟของ sensor แต่ละตัว โดยตั้งให้อัพเดตทุก 5วินาที 
`sensor_to_csv.py` ทำหน้าที่นำไฟล์ JSON ในโฟรเดอร์ curated มาแปลงเป็น csv แล้วเก็บในโฟรเดอร์ warehouse

English Version

This project simulates a factory monitoring system where sensors continuously generate data such as temperature, vibration, and speed.

`sensor_generator.py` simulates streaming sensor data and writes them into the RAW folder.

`sensor_cleaner.py` validates and cleans incoming files from RAW and sends them to STAGING.

`sensor_aggregator.py` reads data from STAGING, aggregates them by sensor_id, and stores the results in CURATED.

An alert system is implemented in `sensor_alert.py` to detect dangerous conditions such as:
- temperature > 90
- vibration > 30
- speed > 1800

When anomalies are detected, alert files are written to the ALERT folder.

`sensor_dashboard.py` visualizes sensor behavior in near real-time, updating every 5 seconds.

Finally, `sensor_to_csv.py` loads curated JSON data into a partitioned CSV warehouse for further analysis.
