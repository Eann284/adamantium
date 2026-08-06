import time
from fastapi.testclient import TestClient
from app.main import app
from app.database import sessionLocal
from app.models.user import UserManager
from app.api.inventory import router as inventory_router
from app.models.product import Product
from app.models.inventory import ProductsInventory
from app.models.stock import Stock
from app.models.logs import Log
from sqlalchemy import text

if not any(hasattr(r, "path") and r.path == "/inventory/" for r in app.routes):
    app.include_router(inventory_router)

client = TestClient(app)

def unique_name(base: str) -> str:
    return f"{base} {int(time.time())}"

def create_test_user(role: str, email: str, password: str):
    response = client.post(
        "/auth/register",
        json={
            "name": f"Test {role}",
            "email": email,
            "password": password,
            "role": role,
            "area": "Laguna"
        }
    )
    return response

def login_user(email: str, password: str):
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password}
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def setup_module(module):
    create_test_user("Admin", "nakyoung@gmail.com", "nakyoung")
    create_test_user("Technician", "hayeon@gmail.com", "hayeon")

def teardown_module(module):
    print("\n=== CLEANING UP INVENTORY TESTS ===")
    db = sessionLocal()
    try:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        db.query(Stock).delete()
        db.query(ProductsInventory).delete()
        db.query(Log).delete()
        db.query(Product).filter(Product.product_name.like("Test%")).delete()
        test_emails = ["nakyoung@gmail.com", "hayeon@gmail.com"]
        db.query(UserManager).filter(UserManager.email.in_(test_emails)).delete()
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.commit()
        print("=== CLEANUP COMPLETE ===")
    except Exception as e:
        print(f"Cleanup error: {e}")
        db.rollback()
    finally:
        db.close()


def test_create_inventory_success():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    product_name = unique_name("Extension")
    create_resp = client.post(
        "/products/",
        json={"product_name": product_name, "product_image": "image.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_resp.status_code == 201, f"Product creation failed: {create_resp.json()}"

    product_data = create_resp.json()
    product_id = product_data["id"]
    assert product_id is not None, f"product_id is None. Response: {product_data}"

    response = client.post(
        "/inventory/add",
        json={
            "product_id": product_id,
            "area": "Quezon",
            "quantity": 100,
            "wh_proof": "Added 100"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == product_id
    assert data["area"] == "Quezon"
    assert data["quantity"] == 100
    assert data["wh_id"] == "nakyoung@gmail.com"
    assert data["new_stock"] == 100

    client.delete(f"/products/{product_id}", headers={"Authorization": f"Bearer {admin_token}"})

def test_add_stock_invalid_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    response = client.post(
        "/inventory/add",
        json={"product_id": 9999, "area": "Cavite", "quantity": 10, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404

def test_add_stock_invalid_area():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    product_name = unique_name("Keyboard")
    create_resp = client.post(
        "/products/",
        json={"product_name": product_name, "product_image": "keyboard.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]
    assert product_id is not None

    response = client.post(
        "/inventory/add",
        json={"product_id": product_id, "area": "InvalidArea", "quantity": 10, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 422

    client.delete(f"/products/{product_id}", headers={"Authorization": f"Bearer {admin_token}"})

def test_add_stock_without_token():
    response = client.post(
        "/inventory/add",
        json={"product_id": 1, "area": "Cavite", "quantity": 10}
    )
    assert response.status_code == 401

def test_add_stock_non_admin():
    tech_token = login_user("hayeon@gmail.com", "hayeon")
    assert tech_token is not None

    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    product_name = unique_name("Monitor")
    create_resp = client.post(
        "/products/",
        json={"product_name": product_name, "product_image": "monitor.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]
    assert product_id is not None

    response = client.post(
        "/inventory/add",
        json={"product_id": product_id, "area": "Cavite", "quantity": 10, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    assert response.status_code == 403
    assert "Admin privileges required" in response.json()["detail"]

    client.delete(f"/products/{product_id}", headers={"Authorization": f"Bearer {admin_token}"})

# ==================== GET TESTS ====================

def test_get_stock_by_area():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    p1_name = unique_name("ProductA")
    resp1 = client.post(
        "/products/",
        json={"product_name": p1_name, "product_image": "producta.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp1.status_code == 201
    p1_id = resp1.json()["id"]
    assert p1_id is not None

    p2_name = unique_name("ProductB")
    resp2 = client.post(
        "/products/",
        json={"product_name": p2_name, "product_image": "productb.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp2.status_code == 201
    p2_id = resp2.json()["id"]
    assert p2_id is not None

    client.post(
        "/inventory/add",
        json={"product_id": p1_id, "area": "Cavite", "quantity": 20, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/inventory/add",
        json={"product_id": p2_id, "area": "Laguna", "quantity": 30, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get(
        "/inventory/area/Cavite",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert item["area"] == "Cavite"
    found = any(item["product_id"] == p1_id for item in data)
    assert found

    client.delete(f"/products/{p1_id}", headers={"Authorization": f"Bearer {admin_token}"})
    client.delete(f"/products/{p2_id}", headers={"Authorization": f"Bearer {admin_token}"})

def test_get_all_inventory():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    p1_name = unique_name("ProdX")
    resp1 = client.post(
        "/products/",
        json={"product_name": p1_name, "product_image": "prodx.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp1.status_code == 201
    p1_id = resp1.json()["id"]
    assert p1_id is not None

    p2_name = unique_name("ProdY")
    resp2 = client.post(
        "/products/",
        json={"product_name": p2_name, "product_image": "prody.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp2.status_code == 201
    p2_id = resp2.json()["id"]
    assert p2_id is not None

    client.post(
        "/inventory/add",
        json={"product_id": p1_id, "area": "Cavite", "quantity": 5, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/inventory/add",
        json={"product_id": p2_id, "area": "Laguna", "quantity": 7, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get(
        "/inventory/all",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    client.delete(f"/products/{p1_id}", headers={"Authorization": f"Bearer {admin_token}"})
    client.delete(f"/products/{p2_id}", headers={"Authorization": f"Bearer {admin_token}"})

def test_get_total_stock():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    p_name = unique_name("TotalTest")
    resp = client.post(
        "/products/",
        json={"product_name": p_name, "product_image": "totaltest.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 201
    p_id = resp.json()["id"]
    assert p_id is not None

    client.post(
        "/inventory/add",
        json={"product_id": p_id, "area": "Cavite", "quantity": 10, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/inventory/add",
        json={"product_id": p_id, "area": "Laguna", "quantity": 20, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get(
        f"/inventory/total/{p_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == p_id
    assert data["total_stock"] == 30

    client.delete(f"/products/{p_id}", headers={"Authorization": f"Bearer {admin_token}"})

def test_get_total_stock_not_found():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    response = client.get(
        "/inventory/total/9999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404

def test_get_stock_by_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    p_name = unique_name("DistTest")
    resp = client.post(
        "/products/",
        json={"product_name": p_name, "product_image": "disttest.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 201
    p_id = resp.json()["id"]
    assert p_id is not None

    client.post(
        "/inventory/add",
        json={"product_id": p_id, "area": "Cavite", "quantity": 5, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/inventory/add",
        json={"product_id": p_id, "area": "Laguna", "quantity": 7, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get(
        f"/inventory/product/{p_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == p_id
    areas = {item["area"]: item["stock"] for item in data["areas"]}
    assert areas.get("Cavite") == 5
    assert areas.get("Laguna") == 7

    client.delete(f"/products/{p_id}", headers={"Authorization": f"Bearer {admin_token}"})

def test_get_inventory_summary():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    p1_name = unique_name("SummaryA")
    resp1 = client.post(
        "/products/",
        json={"product_name": p1_name, "product_image": "summarya.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp1.status_code == 201
    p1_id = resp1.json()["id"]
    assert p1_id is not None

    p2_name = unique_name("SummaryB")
    resp2 = client.post(
        "/products/",
        json={"product_name": p2_name, "product_image": "summaryb.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp2.status_code == 201
    p2_id = resp2.json()["id"]
    assert p2_id is not None

    client.post(
        "/inventory/add",
        json={"product_id": p1_id, "area": "Cavite", "quantity": 10, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/inventory/add",
        json={"product_id": p1_id, "area": "Laguna", "quantity": 20, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/inventory/add",
        json={"product_id": p2_id, "area": "Cavite", "quantity": 30, "wh_proof": "Test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get(
        "/inventory/summary",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "grand_total" in data
    assert data["grand_total"] == 60
    assert len(data["per_area"]) >= 2

    client.delete(f"/products/{p1_id}", headers={"Authorization": f"Bearer {admin_token}"})
    client.delete(f"/products/{p2_id}", headers={"Authorization": f"Bearer {admin_token}"})

def test_get_stock_history():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    p_name = unique_name("HistoryTest")
    resp = client.post(
        "/products/",
        json={"product_name": p_name, "product_image": "historytest.jpg"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 201
    p_id = resp.json()["id"]
    assert p_id is not None

    client.post(
        "/inventory/add",
        json={"product_id": p_id, "area": "Cavite", "quantity": 5, "wh_proof": "First batch"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/inventory/add",
        json={"product_id": p_id, "area": "Laguna", "quantity": 7, "wh_proof": "Second batch"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get(
        "/inventory/history",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    found = any(entry["product_name"] == p_name for entry in data)
    assert found

    client.delete(f"/products/{p_id}", headers={"Authorization": f"Bearer {admin_token}"})

def test_get_stock_history_unauthorized():
    response = client.get("/inventory/history")
    assert response.status_code == 401