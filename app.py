"""Production-ready Flask application with monitoring instrumentation."""

import logging
import os
import sys

from flask import Flask, jsonify
# pyrefly: ignore [missing-import]
from prometheus_flask_exporter import PrometheusMetrics
# pyrefly: ignore [missing-import]
from pythonjsonlogger import jsonlogger


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)

    # --------------- Configuration ---------------
    app.config["ENV"] = os.getenv("FLASK_ENV", "production")
    app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    enable_chaos = os.getenv("ENABLE_CHAOS", "false").lower() == "true"

    # --------------- Structured JSON Logging ---------------
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "timestamp", "levelname": "level"},
    )
    log_handler.setFormatter(formatter)

    app.logger.handlers.clear()
    app.logger.addHandler(log_handler)
    app.logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
    app.logger.propagate = False

    # --------------- Prometheus Metrics ---------------
    PrometheusMetrics(app)  # Auto-instruments all routes, exposes /metrics

    # --------------- Routes ---------------
    @app.route("/")
    def home():
        if enable_chaos:
            import random

            if random.random() < 0.3:
                app.logger.error("Chaos mode: simulated crash triggered")
                return jsonify({"error": "Simulated crash!"}), 500
        app.logger.info("Home endpoint accessed")
        return jsonify({"message": "App is running fine!"})

    @app.route("/health")
    def health():
        """Liveness probe — is the process alive?"""
        return jsonify({"status": "ok"})

    @app.route("/ready")
    def ready():
        """Readiness probe — is the app ready to serve traffic?"""
        # Extend this with DB connectivity checks, cache checks, etc.
        return jsonify({"status": "ready"})

    # --------------- Error Handlers ---------------
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning("Resource not found: %s", error)
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error("Internal server error: %s", error)
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        app.logger.exception("Unhandled exception: %s", error)
        return jsonify({"error": "Unexpected error occurred"}), 500

    app.logger.info("Application initialized", extra={
        "chaos_mode": enable_chaos,
        "environment": app.config["ENV"],
    })

    return app


# --------------- Entrypoint ---------------
app = create_app()

if __name__ == "__main__":
    # Dev-only: use Gunicorn in production (see gunicorn.conf.py)
    print("⚠️  Running with Flask dev server. Use Gunicorn for production.")
    app.run(host="0.0.0.0", port=5000, debug=True)
