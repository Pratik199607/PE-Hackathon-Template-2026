from flask import Flask, request, Response
from dotenv import load_dotenv
import time
import logging

from app.config import Config
from app.database import init_db_with_flask
from app.routes import register_routes

# NEW
from app.core.logger import setup_logger
from app.core.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    ERROR_COUNT,
    metrics_response,
)

def create_app():
    load_dotenv()

    # ✅ Setup logging
    setup_logger()
    logger = logging.getLogger(__name__)

    app = Flask(__name__)
    app.config.from_object(Config)

    init_db_with_flask(app)
    register_routes(app)

    # 🔥 Request Tracking Middleware
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_request(response):
        latency = time.time() - request.start_time

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path
        ).inc()

        REQUEST_LATENCY.labels(
            endpoint=request.path
        ).observe(latency)

        if response.status_code >= 400:
            ERROR_COUNT.labels(endpoint=request.path).inc()

        logger.info(
            f"{request.method} {request.path} {response.status_code} {latency:.3f}s"
        )

        return response

    # ✅ Health Check
    @app.route("/health")
    def health():
        return {"status": "ok"}

    # ✅ Metrics Endpoint
    @app.route("/metrics")
    def metrics():
        return Response(metrics_response(), mimetype="text/plain")

    return app