from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_product_test():
    client.post(
        ""
    )