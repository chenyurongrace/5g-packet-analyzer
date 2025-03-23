import requests
import time
import random

url = "http://localhost:5000"
print("📡 Sending simulated requests to Flask server...")

for i in range(20):
    try:
        r = requests.get(url)
        print(f"✅ Request #{i+1}: Status code {r.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Add burst behavior and irregular timing
    if i % 5 == 0:
        time.sleep(2)  # pause to simulate drop
    else:
        time.sleep(random.uniform(0.1, 0.6))  # simulate jitter

