from flask import Flask, request, abort, Response
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
    IN_PROGRESS,
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
        IN_PROGRESS.inc()  

    @app.after_request
    def log_request(response):
        latency = time.time() - request.start_time

        # Groups /products/1 and /products/99 into /products/<id>
        endpoint = str(request.url_rule) if request.url_rule else request.path

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            http_status=response.status_code
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(latency)

        if response.status_code >= 400:
            ERROR_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                http_status=response.status_code
            ).inc()

        IN_PROGRESS.dec()

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

    # ✅ Error Endpoint
    @app.route("/error")
    def error():
        abort(500)

    return app