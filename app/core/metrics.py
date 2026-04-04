from prometheus_client import Counter, Histogram, Gauge, generate_latest
import psutil
import time

# 🔥 Golden Signals
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP Requests", ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency", ["endpoint"]
)

ERROR_COUNT = Counter(
    "http_errors_total", "Total Errors", ["endpoint"]
)

CPU_USAGE = Gauge("cpu_usage_percent", "CPU usage")
MEMORY_USAGE = Gauge("memory_usage_percent", "Memory usage")


def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)


def metrics_response():
    update_system_metrics()
    return generate_latest()