import time
import json
import random
from datetime import datetime

# List of possible feedback messages with associated sentiment scores
FEEDBACK_OPTIONS = [
    ("Great service!", 0.8),    # Positive
    ("Very good!", 0.6),        # Positive
    ("It's okay.", 0.0),        # Neutral
    ("Too expensive!", -0.5),   # Negative
    ("Poor service.", -0.8)     # Negative
]

def produce_logs():
    print("Producer thread started successfully.")
    while True:
        feedback, sentiment = random.choice(FEEDBACK_OPTIONS)
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": "/weather",
            "user_feedback": feedback,
            "sentiment": sentiment
        }
        print(f"Produced: {json.dumps(log_entry)}")
        # Simulate storing the sentiment for the endpoint
        try:
            from scripts.pricing_engine import sentiment_scores
            sentiment_scores["/weather"] = sentiment  # Update the shared sentiment score
        except ImportError:
            from pricing_engine import sentiment_scores
            sentiment_scores["/weather"] = sentiment
        time.sleep(5)