# Simple payments resource — mock implementation
# used as a realistic API endpoint for pipeline testing

from flask import Blueprint, jsonify, request
import uuid

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/payments", methods=["POST"])
def create_payment():
    data = request.get_json()

    if not data or "amount" not in data or "currency" not in data:
        return jsonify({"error": "amount and currency are required"}), 400

    # Mock payment processing
    transaction_id = str(uuid.uuid4())
    return jsonify({
        "transaction_id": transaction_id,
        "amount": data["amount"],
        "currency": data["currency"],
        "status": "processed"
    }), 201

@payments_bp.route("/payments/<transaction_id>", methods=["GET"])
def get_payment(transaction_id):
    # Mock lookup
    return jsonify({
        "transaction_id": transaction_id,
        "status": "processed"
    }), 200
