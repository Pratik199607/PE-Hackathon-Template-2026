from prometheus_client import Counter, Histogram, Gauge, generate_latest
import psutil
import time

# 🔥 Golden Signals
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency", ["method","endpoint"]
)

ERROR_COUNT = Counter(
    "http_errors_total", "Total Errors", ["method", "endpoint", "http_status"]
)

CPU_USAGE = Gauge("cpu_usage_percent", "CPU usage")
MEMORY_USAGE = Gauge("memory_usage_percent", "Memory usage")

# Saturation (app-level)
IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "In-progress requests"
)

def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent(interval=0.5))
    MEMORY_USAGE.set(psutil.virtual_memory().percent)


def metrics_response():
    update_system_metrics()
    return generate_latest()