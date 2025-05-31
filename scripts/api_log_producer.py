import time
import json
from datetime import datetime

def produce_logs():
    print("Producer thread started successfully.")
    while True:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": "/weather",
            "user_feedback": "Great service!"
        }
        print(f"Produced: {json.dumps(log_entry)}")
        time.sleep(5)