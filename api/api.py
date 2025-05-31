from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import numpy as np
import os
import requests
import threading
from stable_baselines3 import PPO
import gymnasium as gym

# Local imports with error handling
try:
    from scripts.pricing_engine import (
        prices, request_counts,
        sentiment_scores, competitor_prices,
        get_dashboard_html
    )
    from scripts.api_log_producer import produce_logs
except ImportError:
    from pricing_engine import (
        prices, request_counts,
        sentiment_scores, competitor_prices,
        get_dashboard_html
    )
    from api_log_producer import produce_logs

app = FastAPI()

# Add a root route for health checks
@app.get("/")
async def root():
    return {"status": "healthy"}

# Download the PPO model at startup
MODEL_URL = "https://github.com/777Hans/Dynamic-Pricing-Engine/releases/download/v1.0/ppo_model.zip"
MODEL_PATH = "models/ppo_model.zip"

if not os.path.exists(MODEL_PATH):
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)

# Load the PPO model
try:
    model = PPO.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.on_event("startup")
async def startup_event():
    # Start the log producer thread
    producer_thread = threading.Thread(target=produce_logs)
    producer_thread.daemon = True
    producer_thread.start()

@app.get("/api/price")
async def get_price(endpoint: str = "/weather"):
    try:
        # Update metrics
        request_counts[endpoint] = request_counts.get(endpoint, 0) + 1
        # Sentiment score is now updated by the log producer, use the current value
        current_sentiment = sentiment_scores.get(endpoint, 0.0)
        competitor_prices[endpoint] = competitor_prices.get(endpoint, 0.5)

        # Use the PPO model for prediction
        if model is None:
            price = 0.5  # Fallback if model loading failed
        else:
            obs = np.array([
                request_counts[endpoint],
                current_sentiment,
                competitor_prices[endpoint]
            ], dtype=np.float32)
            action, _ = model.predict(obs)
            price = action[0] * 0.1 + 0.1  # Scale action to price

        prices[endpoint] = price

        return {
            "endpoint": endpoint,
            "price": price,
            "demand": request_counts[endpoint],
            "sentiment": current_sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    try:
        return get_dashboard_html()
    except Exception as e:
        return f"Error: {str(e)}"

from mangum import Mangum
handler = Mangum(app)