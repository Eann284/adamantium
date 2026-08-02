from fastapi.testclient import TestClient
from app.main import app
from app.database import sessionLocal
from app.models.user import UserManager
from app.api.stock import router as stock_router
from app.models.product import Product


# Force register stock router
if not any(hasattr(r, "path") and r.path == "/stock/" for r in app.routes):
    app.include_router(stock_router)

client = TestClient(app)

def create_test_user(role:str, email:str, password:str):
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
       data={
            "username": email,
            "password": password
        }
    )
    return response.json().get("access_token")



def setup_module(module):
    create_test_user("Admin", "nakyoung@gmail.com", "nakyoung")

    create_test_user("Technician", "hayeon@gmail.com", "hayeon")

    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    product_response = client.post(
        "/products/",
        json={"product_name": "Laptop Charger", "product_image": "cable.jpg", "stock": 0},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert product_response.status_code == 201, f"Failed to create product: {product_response.json()}"
    print(f"Created product with ID: {product_response.json()['id']}")
    
    print("=== STOCK TEST SETUP COMPLETE ===")


# Adding stock
def test_add_stock_success():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    products_response = client.get(
        "/products/",
        headers={"Authorization":f"Bearer {admin_token}"}

    )
    products = products_response.json()
    product_id = products[0]["id"]

    response = client.post(
        "/stock/",
        json={
            "product_id": product_id,
            "quantity": 100,
            "wh_proof": "Purchased from PC Express"
        },
        headers={"Authorization":f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 100
    assert data["product_id"] == product_id
    assert data["wh_id"] == "nakyoung@gmail.com"
    assert "wh_logs" in data
    assert "date" in data

    product = client.get(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    ).json()
    assert product["stock"] == 100


def test_add_stock_anytime():
    """Admin can add stock even if stock already exists"""
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    
    # Get product ID
    products_response = client.get(
        "/products/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product_id = products_response.json()[0]["id"]
    
    # First add stock
    response1 = client.post(
        "/stock/",
        json={
            "product_id": product_id,
            "quantity": 25,
            "wh_proof": "First restock"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response1.status_code == 201
    assert response1.json()["quantity"] == 25
    
    # Second add stock (should work even though stock > 0)
    response2 = client.post(
        "/stock/",
        json={
            "product_id": product_id,
            "quantity": 75,
            "wh_proof": "Second restock"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response2.status_code == 201
    assert response2.json()["quantity"] == 75
    
    # Verify final stock is 75 (overwrites, doesn't add)
    product = client.get(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    ).json()
    assert product["stock"] == 75


def test_add_stock_invalid_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    response = client.post(
        "/stock/",

        json={
            "product_id": 900,
            "quantity": 90,
            "wh_proof": "Invalid"   
        },
        headers={"Authorization": f"Bearer {admin_token}"}

    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_add_stock_unauthorized():
    """Returns 401 if not authenticated"""
    response = client.post(
        "/stock/",
        json={
            "product_id": 1,
            "quantity": 10
        }
    )
    assert response.status_code == 401

def test_add_stock_non_admin():
    """Returns 403 if user is not Admin"""
    # Login as technician
    tech_token = login_user("hayeon@gmail.com", "hayeon")
    
    response = client.post(
        "/stock/",
        json={
            "product_id": 1,
            "quantity": 10
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    
    assert response.status_code == 403
    assert "Admin privileges required" in response.json()["detail"]


# getting logs 

def test_get_logs_success():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    products_response = client.get(
        "/products/",
        headers={"Authorization": f"Bearer {admin_token}"}

    )
    products = products_response.json()
    product_id = products[0]["id"]

    client.post(
        "/products/",
        json={"product_id": product_id, "quantity": 100, "wh_proof": "Log test"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get(
        "/stock/logs",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    logs = response.json()
    assert isinstance(logs, list)
    assert len(logs) > 0

    first_log = logs[0]
    assert "id" in first_log
    assert "wh_email" in first_log
    assert "date" in first_log
    assert "wh_proof" in first_log
    assert first_log["wh_email"] == "nakyoung@gmail.com"

def test_get_logs_pagination():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    products_response = client.get(
        "/products/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    products = products_response.json()
    product_id = products[0]["id"]

    for x in range(3):
       client.post(
            "/stock/",
            json={"product_id": product_id, "quantity": 10 + x, "wh_proof": f"Log {x}"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )

    response = client.get(
        "/stock/logs?skip=1&limit=2",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) <= 2


def test_get_all_stock():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    response = client.get(
        "/stock/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    stock_data = response.json()
    assert isinstance(stock_data, list)

    for item in stock_data:
        assert "id" in item
        assert "product_name" in item
        assert "stock" in item

def test_get_all_stock_unauthorized():
    """Returns 401 if not authenticated for all stock view"""
    response = client.get("/stock/")
    assert response.status_code == 401

def teardown_module(module):
    """Clean up test data after all tests"""
    print("\n=== CLEANING UP STOCK TESTS ===")
    db = sessionLocal()
    try:
        # Delete test users
        test_emails = ["nakyoung@gmail.com", "hayeon@gmail.com"]
        db.query(UserManager).filter(UserManager.email.in_(test_emails)).delete()
        # Delete products created in test (optional)
        db.query(Product).filter(Product.product_name.like("Test%")).delete()
        # Delete logs and stock entries (cascade will handle)
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()
    print("=== CLEANUP COMPLETE ===")