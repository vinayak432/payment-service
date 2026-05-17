def test_create_payment_success(client):
    payload = {"amount": 100.00, "currency": "USD"}
    response = client.post("/api/v1/payments", json=payload)
    assert response.status_code == 201
    assert "transaction_id" in response.json
    assert response.json["status"] == "processed"

def test_create_payment_missing_fields(client):
    response = client.post("/api/v1/payments", json={"amount": 50})
    assert response.status_code == 400
    assert "error" in response.json
