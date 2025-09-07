from flask import Flask, request, Response, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time, random

app = Flask(__name__)

# --- Prometheus metrics ---
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5)
)

IN_PROGRESS = Gauge("inprogress_requests", "In-progress HTTP requests")

def _record(response):
    # Called from after_request to record per-request metrics
    try:
        endpoint = request.path
        REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    except Exception:
        pass
    return response

@app.before_request
def _before():
    request._start_time = time.time()
    IN_PROGRESS.inc()

@app.after_request
def _after(response):
    try:
        latency = time.time() - getattr(request, "_start_time", time.time())
        REQUEST_LATENCY.labels(request.path).observe(latency)
    except Exception:
        pass
    IN_PROGRESS.dec()
    return _record(response)

@app.route("/")
def home():
    return jsonify(message="Hello from demo app 👋"), 200

@app.route("/work")
def do_work():
    # Simulate variable work
    n = random.randint(10000, 50000)
    s = 0
    for i in range(n):
        s += i*i
    return jsonify(result=s, did="cpu-work", n=n), 200

@app.route("/error")
def sometimes_error():
    # return 500 ~20% of the time
    if random.random() < 0.2:
        return jsonify(error="simulated failure"), 500
    return jsonify(ok=True), 200

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
