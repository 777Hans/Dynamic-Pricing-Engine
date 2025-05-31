# Global state for metrics
prices = {}
request_counts = {}
sentiment_scores = {}
competitor_prices = {}

def get_dashboard_html():
    html = "<html><body><h1>Dynamic Pricing Dashboard</h1><table border='1'>"
    html += "<tr><th>Endpoint</th><th>Price</th><th>Demand</th><th>Sentiment</th><th>Competitor Price</th></tr>"
    for endpoint in prices:
        html += f"<tr><td>{endpoint}</td><td>{prices[endpoint]}</td><td>{request_counts.get(endpoint, 0)}</td><td>{sentiment_scores.get(endpoint, 0.0)}</td><td>{competitor_prices.get(endpoint, 0.0)}</td></tr>"
    html += "</table></body></html>"
    return html