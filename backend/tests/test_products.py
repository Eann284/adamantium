import time
from fastapi.testclient import TestClient
from app.main import app
from app.database import sessionLocal
from app.models.user import UserManager
from app.api.products import router as products_router
from app.models.product import Product
from sqlalchemy import text

# Force register products router
if not any(hasattr(r, "path") and r.path == "/products/" for r in app.routes):
    app.include_router(products_router)

client = TestClient(app)

# ==================== HELPERS ====================

def unique_name(base: str) -> str:
    """Generate a unique product name with timestamp"""
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
        data={
            "username": email,
            "password": password
        }
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

# ==================== SETUP ====================

def setup_module(module):
    create_test_user("Admin", "nakyoung@gmail.com", "nakyoung")
    create_test_user("Technician", "hayeon@gmail.com", "hayeon")


# ==================== CREATE TESTS ====================

def test_create_product_success():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    name = unique_name("Type C Charger")

    response = client.post(
        "/products/",
        json={
            "product_name": name,
            "product_image": "typec.jpg",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["product_name"] == name
    assert data["product_image"] == "typec.jpg"

    # Cleanup
    client.delete(f"/products/{data['id']}", headers={"Authorization": f"Bearer {admin_token}"})


def test_create_existing_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    name = unique_name("USB Cable")

    # First product – success
    product_1 = client.post(
        "/products/",
        json={
            "product_name": name,
            "product_image": "usb.jpg",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert product_1.status_code == 201
    data = product_1.json()
    product_id = data["id"]

    # Second product with same name – should fail
    product_2 = client.post(
        "/products/",
        json={
            "product_name": name,
            "product_image": "usb.jpg",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert product_2.status_code == 400
    assert "product with this name already exists" in product_2.json()["detail"].lower()

    # Cleanup
    client.delete(f"/products/{product_id}", headers={"Authorization": f"Bearer {admin_token}"})


def test_create_product_fail():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    response = client.post(
        "/products/",
        json={
            "product_name": None,
            "product_image": "docking.jpg",
            
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 422
    data = response.json()
    assert "product_name" in str(data).lower()


def test_create_product_as_non_admin():
    technician_token = login_user("hayeon@gmail.com", "hayeon")
    assert technician_token is not None

    response = client.post(
        "/products/",
        json={
            "product_name": "Test Adaptor",
            "product_image": "adaptor.jpg",
            
        },
        headers={"Authorization": f"Bearer {technician_token}"}
    )

    assert response.status_code == 403


# ==================== UPDATE TESTS ====================

def test_update_product_success():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    name = unique_name("Wireless Mouse")

    # Create product
    create_resp = client.post(
        "/products/",
        json={
            "product_name": name,
            "product_image": "wireless.jpg",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]

    # Update product
    update = client.put(
        f"/products/{product_id}",
        json={
            "product_name": f"{name} --EDITED",
            "product_image": "wireless.jpg",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert update.status_code == 200
    data = update.json()
    assert data["product_name"] == f"{name} --EDITED"

    # Cleanup
    client.delete(f"/products/{product_id}", headers={"Authorization": f"Bearer {admin_token}"})


def test_update_nonexistent_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    product_id = 999  # This ID doesn't exist

    update = client.put(
        f"/products/{product_id}",
        json={
            "product_name": "Test Wireless Keyboard --EDITED",
            "product_image": "wireless.jpg",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert update.status_code == 404
    assert "product with this id does not exist" in update.json()["detail"].lower()


def test_update_product_as_non_admin():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    name = unique_name("Wireless Mouse")


    create_resp = client.post(
        "/products/",
        json={
            "product_name": name,
            "product_image": "wireless.jpg",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]

    # ✅ Technician tries to update
    technician_token = login_user("hayeon@gmail.com", "hayeon")
    assert technician_token is not None

    update = client.put(
        f"/products/{product_id}",
        json={
            "product_name": f"{name} --EDITED",
            "product_image": "wireless.jpg",
        },
        headers={"Authorization": f"Bearer {technician_token}"}
    )

    assert update.status_code == 403

    # Cleanup
    client.delete(f"/products/{product_id}", headers={"Authorization": f"Bearer {admin_token}"})


# ==================== DELETE TESTS ====================

def test_delete_product_success():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    name = unique_name("ASUS Laptop")

    response = client.post(
        "/products/",
        json={
            "product_name": name,
            "product_image": "asus.jpg",
           
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    product_id = data["id"]

    delete = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert delete.status_code in [200, 204]

    get_resp = client.get(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_resp.status_code == 404


def test_delete_nonexistent_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    product_id = 800

    delete = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert delete.status_code == 404


# ==================== GET TESTS ====================

def test_get_all_products():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    products = client.get(
        "/products/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert products.status_code == 200
    assert isinstance(products.json(), list)


def test_get_all_products_as_non_admin():
    technician_token = login_user("hayeon@gmail.com", "hayeon")
    assert technician_token is not None

    products = client.get(
        "/products/",
        headers={"Authorization": f"Bearer {technician_token}"}
    )

    assert products.status_code == 200
    assert isinstance(products.json(), list)


def test_get_all_products_no_auth():
    # ✅ Your API allows public GET, so expect 200
    products = client.get("/products/")
    assert products.status_code == 200
    assert isinstance(products.json(), list)


def test_get_product_by_id():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    name = unique_name("DELL Laptop")

    response = client.post(
        "/products/",
        json={
            "product_name": name,
            "product_image": "dell.jpg",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    product_id = data["id"]

    product = client.get(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert product.status_code == 200
    product_data = product.json()
    assert product_data["product_name"] == name
    assert product_data["product_image"] == "dell.jpg"

    # Cleanup
    client.delete(f"/products/{product_id}", headers={"Authorization": f"Bearer {admin_token}"})


def test_get_nonexistent_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
    assert admin_token is not None

    product_id = 700

    product = client.get(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert product.status_code == 404


# ==================== TEARDOWN ====================

def teardown_module(module):
    """Clean up all test data after all tests"""
    print("\n=== CLEANING UP PRODUCT TESTS ===")
    db = sessionLocal()
    try:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        # Delete child tables
        from app.models.release import Release
        from app.models.stock import Stock
        from app.models.logs import Log
        from app.models.material_request import MaterialRequest

        db.query(Release).delete()
        db.query(Stock).delete()
        db.query(Log).delete()
        db.query(MaterialRequest).delete()

        # Delete test products
        db.query(Product).filter(Product.product_name.like("Test%")).delete()

        # Delete test users
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