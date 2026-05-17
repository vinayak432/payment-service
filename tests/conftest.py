import pytest
from app import create_app

@pytest.fixture(scope="session")
def app():
    """
    Session-scoped fixture — app created ONCE for the entire test run.
    This prevents multiple create_app() calls hitting the Prometheus registry.
    """
    app = create_app()
    app.config["TESTING"] = True
    yield app

@pytest.fixture(scope="session")
def client(app):
    """HTTP test client, also session-scoped."""
    return app.test_client()
