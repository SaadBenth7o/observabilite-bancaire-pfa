import logging, sys, os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from elasticapm.contrib.flask import ElasticAPM
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response, request
from pythonjsonlogger import jsonlogger

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
apm = ElasticAPM()

# Prometheus metrics
REQUEST_COUNT = Counter("flask_http_request_total", "Total HTTP requests", ["method","endpoint","http_status"])
REQUEST_LATENCY = Histogram("flask_request_latency_seconds", "Request latency", ["endpoint"])

class PrometheusMetrics:
    def init_app(self, app):
        @app.after_request
        def after_request(response):
            REQUEST_COUNT.labels(request.method, request.endpoint or "unknown", response.status_code).inc()
            return response

        @app.route("/metrics")
        def metrics():
            return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

prometheus_metrics = PrometheusMetrics()

def init_logging(app):
    log_level = getattr(logging, app.config.get("LOG_LEVEL","INFO").upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # JSON formatter
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    # Stream handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # File handler
    os.makedirs("/app/logs", exist_ok=True)
    fh = logging.FileHandler("/app/logs/app.json.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
