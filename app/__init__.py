from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import CollectorRegistry, REGISTRY

# Module-level guard — metrics registered only once per process
_metrics = None

def create_app(test_config=None):
    app = Flask(__name__)

    global _metrics
    if _metrics is None:
        _metrics = PrometheusMetrics(app)
        _metrics.info("app_info", "Payment service info", version="1.0.0")
    else:
        # Re-bind the existing metrics object to this new app instance
        _metrics.init_app(app)

    from app.routes.health import health_bp
    from app.routes.payments import payments_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(payments_bp, url_prefix="/api/v1")

    return app
