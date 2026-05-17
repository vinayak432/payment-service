from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def liveness():
    """Kubernetes liveness probe — is the process alive?"""
    return jsonify({"status": "ok"}), 200

@health_bp.route("/ready")
def readiness():
    """Kubernetes readiness probe — is the app ready to serve traffic?"""
    return jsonify({"status": "ready", "service": "payment-service"}), 200
