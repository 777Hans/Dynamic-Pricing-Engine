import time
import json
import random
from datetime import datetime
import numpy as np
from stable_baselines3 import PPO

# List of possible feedback messages with associated sentiment scores
FEEDBACK_OPTIONS = [
    ("Great service!", 0.8),    # Positive
    ("Very good!", 0.6),        # Positive
    ("It's okay.", 0.0),        # Neutral
    ("Too expensive!", -0.5),   # Negative
    ("Poor service.", -0.8)     # Negative
]

def produce_logs(model):
    print("Producer thread started successfully.")
    while True:
        feedback, sentiment = random.choice(FEEDBACK_OPTIONS)
        endpoint = "/weather"
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": endpoint,
            "user_feedback": feedback,
            "sentiment": sentiment
        }
        print(f"Produced: {json.dumps(log_entry)}")
        try:
            from scripts.pricing_engine import (
                prices, request_counts,
                sentiment_scores, competitor_prices,
                historical_data, save_data, trim_historical_data
            )
            # Update sentiment and recalculate price
            sentiment_scores[endpoint] = sentiment
            request_counts[endpoint] = request_counts.get(endpoint, 0) + 1
            competitor_prices[endpoint] = competitor_prices.get(endpoint, 0.5)

            # Recalculate price using the PPO model
            if model is None:
                price = 0.5  # Fallback
            else:
                obs = np.array([
                    request_counts[endpoint],
                    sentiment_scores[endpoint],
                    competitor_prices[endpoint]
                ], dtype=np.float32)
                action, _ = model.predict(obs)
                price = action[0] * 0.1 + 0.1  # Scale action to price
                price = round(price, 2)

            prices[endpoint] = price

            # Store historical data
            if endpoint not in historical_data:
                historical_data[endpoint] = []
            historical_data[endpoint].append({
                "timestamp": log_entry["timestamp"],
                "price": price,
                "demand": request_counts[endpoint],
                "sentiment": sentiment,
                "competitor_price": competitor_prices[endpoint],
                "user_feedback": feedback
            })
            print(f"Appended to historical_data: {historical_data[endpoint][-1]}")  # Debug log

            # Trim historical data
            trim_historical_data()

            # Save updated data
            save_data(prices, request_counts, sentiment_scores, competitor_prices, historical_data)
        except ImportError:
            from pricing_engine import (
                prices, request_counts,
                sentiment_scores, competitor_prices,
                historical_data, save_data, trim_historical_data
            )
            sentiment_scores[endpoint] = sentiment
            request_counts[endpoint] = request_counts.get(endpoint, 0) + 1
            competitor_prices[endpoint] = competitor_prices.get(endpoint, 0.5)

            if model is None:
                price = 0.5
            else:
                obs = np.array([
                    request_counts[endpoint],
                    sentiment_scores[endpoint],
                    competitor_prices[endpoint]
                ], dtype=np.float32)
                action, _ = model.predict(obs)
                price = action[0] * 0.1 + 0.1
                price = round(price, 2)

            prices[endpoint] = price

            if endpoint not in historical_data:
                historical_data[endpoint] = []
            historical_data[endpoint].append({
                "timestamp": log_entry["timestamp"],
                "price": price,
                "demand": request_counts[endpoint],
                "sentiment": sentiment,
                "competitor_price": competitor_prices[endpoint],
                "user_feedback": feedback
            })
            print(f"Appended to historical_data (fallback): {historical_data[endpoint][-1]}")  # Debug log

            trim_historical_data()

            save_data(prices, request_counts, sentiment_scores, competitor_prices, historical_data)

        time.sleep(10)  # Increased to 10 seconds