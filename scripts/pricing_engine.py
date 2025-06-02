import json
import os

# File paths for persistence
DATA_FILE = "pricing_data.json"

# Load data from file if it exists
def load_data():
    # Temporarily disable loading from file
    return {}, {}, {}, {}, {}
    # if os.path.exists(DATA_FILE):
    #     with open(DATA_FILE, "r") as f:
    #         data = json.load(f)
    #         return (
    #             data.get("prices", {}),
    #             data.get("request_counts", {}),
    #             data.get("sentiment_scores", {}),
    #             data.get("competitor_prices", {}),
    #             data.get("historical_data", {})
    #         )
    # return {}, {}, {}, {}, {}

# Save data to file
def save_data(prices, request_counts, sentiment_scores, competitor_prices, historical_data):
    # Temporarily disable saving to file
    pass
    # data = {
    #     "prices": prices,
    #     "request_counts": request_counts,
    #     "sentiment_scores": sentiment_scores,
    #     "competitor_prices": competitor_prices,
    #     "historical_data": historical_data
    # }
    # with open(DATA_FILE, "w") as f:
    #     json.dump(data, f)

# Global state for metrics
prices, request_counts, sentiment_scores, competitor_prices, historical_data = load_data()

def trim_historical_data():
    # Keep only the most recent 20 entries per endpoint
    for endpoint in historical_data:
        if len(historical_data[endpoint]) > 20:
            historical_data[endpoint] = historical_data[endpoint][-20:]

def get_dashboard_html():
    trim_historical_data()  # Trim before rendering
    html = "<html><head><title>Dynamic Pricing Dashboard</title>"
    html += "<script>function autoRefresh() { window.location.reload(); } setInterval(autoRefresh, 10000);</script>"
    html += "</head><body><h1>Dynamic Pricing Dashboard</h1><table border='1'>"
    html += "<tr><th>Timestamp</th><th>Endpoint</th><th>Price</th><th>Demand</th><th>Sentiment</th><th>Competitor Price</th><th>Feedback</th></tr>"
    for endpoint in historical_data:
        for entry in historical_data[endpoint]:
            html += f"<tr><td>{entry['timestamp']}</td><td>{endpoint}</td><td>{entry['price']:.2f}</td><td>{entry['demand']}</td><td>{entry['sentiment']}</td><td>{entry['competitor_price']}</td><td>{entry.get('user_feedback', 'N/A')}</td></tr>"
    html += "</table></body></html>"
    return html