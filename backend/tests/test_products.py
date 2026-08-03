import time
from fastapi.testclient import TestClient
from app.main import app
from app.database import sessionLocal
from app.models.user import UserManager
from app.api.material_request import router as material_request_router
from app.models.product import Product
from app.models.release import Release
from sqlalchemy import text

# Force register router
if not any(hasattr(r, "path") and r.path == "/requests/" for r in app.routes):
    app.include_router(material_request_router)

client = TestClient(app)

# ==================== HELPERS ====================

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
            "area": "Cavite"
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

def create_product(name: str, stock: int = 200, admin_token: str = None) -> int:
    """Create a product and return its ID."""
    if admin_token is None:
        admin_token = login_user("peter@gmail.com", "peter")
    response = client.post(
        "/products/",
        json={
            "product_name": unique_name(name),
            "product_image": f"{name.lower()}.jpg",
            "stock": stock
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201, f"Failed to create product: {response.json()}"
    return response.json()["id"]

def delete_product(product_id: int, admin_token: str = None):
    """Delete a product by ID."""
    if admin_token is None:
        admin_token = login_user("peter@gmail.com", "peter")
    client.delete(f"/products/{product_id}", headers={"Authorization": f"Bearer {admin_token}"})

# ==================== SETUP ====================

def setup_module(module):
    # Create all needed users once
    create_test_user("Admin", "peter@gmail.com", "peter")
    create_test_user("Technician", "sohyun@gmail.com", "sohyun")
    create_test_user("Supervisor", "hina@gmail.com", "hina")
    create_test_user("Custodian", "steve@gmail.com", "steve")

def teardown_module(module):
    # Safety cleanup: delete any leftover test products
    db = sessionLocal()
    try:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        db.query(Product).filter(Product.product_name.like("Test%")).delete()
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.commit()
    except Exception as e:
        print(f"Teardown error: {e}")
        db.rollback()
    finally:
        db.close()

# ==================== TECHNICIAN TESTS ====================

def test_technician_create_request():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("Mouse", admin_token=admin_token)
    p2_id = create_product("Mousepad", admin_token=admin_token)

    token = login_user("sohyun@gmail.com", "sohyun")
    assert token is not None

    response = client.post(
        "/requests/",
        json={
            "items": [
                {"product_id": p1_id, "quantity": 2},
                {"product_id": p2_id, "quantity": 3}
            ],
            "mrf_files": "photo1.jpg,photo2.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["requestor_email"] == "sohyun@gmail.com"
    assert data["approval_status"] == "Pending"
    assert data["release_status"] == "Pending"
    assert len(data["items"]) == 2

    delete_product(p1_id, admin_token)
    delete_product(p2_id, admin_token)

def test_technician_create_request_invalid_product():
    token = login_user("sohyun@gmail.com", "sohyun")
    assert token is not None

    response = client.post(
        "/requests/",
        json={
            "items": [{"product_id": 999, "quantity": 2}],
            "mrf_files": "photo.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_technician_view_my_requests():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("ViewTest", admin_token=admin_token)

    token = login_user("sohyun@gmail.com", "sohyun")
    assert token is not None

    client.post(
        "/requests/",
        json={
            "items": [{"product_id": p1_id, "quantity": 1}],
            "mrf_files": "view.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get(
        "/requests/sent",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    delete_product(p1_id, admin_token)

# ==================== SUPERVISOR TESTS ====================

def test_supervisor_view_pending():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("PendingTest", admin_token=admin_token)

    tech_token = login_user("sohyun@gmail.com", "sohyun")
    assert tech_token is not None

    client.post(
        "/requests/",
        json={
            "items": [{"product_id": p1_id, "quantity": 1}],
            "mrf_files": "pending.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    sup_token = login_user("hina@gmail.com", "hina")
    assert sup_token is not None

    response = client.get(
        "/requests/pending",
        headers={"Authorization": f"Bearer {sup_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    delete_product(p1_id, admin_token)

def test_supervisor_approve_request():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("ApproveTest", admin_token=admin_token)

    tech_token = login_user("sohyun@gmail.com", "sohyun")
    assert tech_token is not None

    create_resp = client.post(
        "/requests/",
        json={
            "items": [{"product_id": p1_id, "quantity": 2}],
            "mrf_files": "approve.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    assert create_resp.status_code == 201
    mrf_id = create_resp.json()["mrf_id"]

    sup_token = login_user("hina@gmail.com", "hina")
    assert sup_token is not None

    response = client.put(
        f"/requests/{mrf_id}/approve",
        headers={"Authorization": f"Bearer {sup_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["approval_status"] == "Approved"
    assert data["approved_by"] == "hina@gmail.com"

    # Clean up: delete the product (we didn't delete the request, but the product cascade will handle it if cascade is set)
    delete_product(p1_id, admin_token)

def test_supervisor_disapprove_request():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("DisapproveTest", admin_token=admin_token)

    tech_token = login_user("sohyun@gmail.com", "sohyun")
    assert tech_token is not None

    create_resp = client.post(
        "/requests/",
        json={
            "items": [{"product_id": p1_id, "quantity": 3}],
            "mrf_files": "disapprove.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    assert create_resp.status_code == 201
    mrf_id = create_resp.json()["mrf_id"]

    sup_token = login_user("hina@gmail.com", "hina")
    assert sup_token is not None

    response = client.put(
        f"/requests/{mrf_id}/disapprove",
        headers={"Authorization": f"Bearer {sup_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["approval_status"] == "Not Approved"

    delete_product(p1_id, admin_token)

def test_supervisor_edit_request():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("EditTest1", admin_token=admin_token)
    p2_id = create_product("EditTest2", admin_token=admin_token)

    tech_token = login_user("sohyun@gmail.com", "sohyun")
    assert tech_token is not None

    create_resp = client.post(
        "/requests/",
        json={
            "items": [{"product_id": p1_id, "quantity": 2}],
            "mrf_files": "edit.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    assert create_resp.status_code == 201
    mrf_id = create_resp.json()["mrf_id"]

    sup_token = login_user("hina@gmail.com", "hina")
    assert sup_token is not None

    response = client.put(
        f"/requests/{mrf_id}/edit",
        json=[
            {"product_id": p1_id, "quantity": 5},
            {"product_id": p2_id, "quantity": 3}
        ],
        headers={"Authorization": f"Bearer {sup_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    for item in data["items"]:
        if item["product_id"] == p1_id:
            assert item["quantity"] == 5

    delete_product(p1_id, admin_token)
    delete_product(p2_id, admin_token)

# ==================== CUSTODIAN TESTS ====================

def test_custodian_view_approved_requests():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("CustViewTest", admin_token=admin_token)

    tech_token = login_user("sohyun@gmail.com", "sohyun")
    assert tech_token is not None

    create_resp = client.post(
        "/requests/",
        json={
            "items": [{"product_id": p1_id, "quantity": 1}],
            "mrf_files": "custview.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    assert create_resp.status_code == 201
    mrf_id = create_resp.json()["mrf_id"]

    sup_token = login_user("hina@gmail.com", "hina")
    assert sup_token is not None
    client.put(
        f"/requests/{mrf_id}/approve",
        headers={"Authorization": f"Bearer {sup_token}"}
    )

    cust_token = login_user("steve@gmail.com", "steve")
    assert cust_token is not None

    response = client.get(
        "/requests/approved",
        headers={"Authorization": f"Bearer {cust_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    delete_product(p1_id, admin_token)

def test_custodian_release_request():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("ReleaseTest", admin_token=admin_token)

    tech_token = login_user("sohyun@gmail.com", "sohyun")
    assert tech_token is not None

    create_resp = client.post(
        "/requests/",
        json={
            "items": [{"product_id": p1_id, "quantity": 2}],
            "mrf_files": "release.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    assert create_resp.status_code == 201
    mrf_id = create_resp.json()["mrf_id"]

    sup_token = login_user("hina@gmail.com", "hina")
    assert sup_token is not None
    client.put(
        f"/requests/{mrf_id}/approve",
        headers={"Authorization": f"Bearer {sup_token}"}
    )

    cust_token = login_user("steve@gmail.com", "steve")
    assert cust_token is not None

    response = client.put(
        f"/requests/{mrf_id}/release",
        headers={"Authorization": f"Bearer {cust_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["release_status"] == "Released"
    assert data["released_by"] == "steve@gmail.com"

    # Manually delete the releases to avoid FK constraint when deleting product
    db = SessionLocal()
    try:
        db.query(Release).filter(Release.mrf_id == mrf_id).delete()
        db.commit()
    finally:
        db.close()

    delete_product(p1_id, admin_token)

def test_custodian_reject_request():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("RejectTest", admin_token=admin_token)

    tech_token = login_user("sohyun@gmail.com", "sohyun")
    assert tech_token is not None

    create_resp = client.post(
        "/requests/",
        json={
            "items": [{"product_id": p1_id, "quantity": 3}],
            "mrf_files": "reject.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    assert create_resp.status_code == 201
    mrf_id = create_resp.json()["mrf_id"]

    sup_token = login_user("hina@gmail.com", "hina")
    assert sup_token is not None
    client.put(
        f"/requests/{mrf_id}/approve",
        headers={"Authorization": f"Bearer {sup_token}"}
    )

    cust_token = login_user("steve@gmail.com", "steve")
    assert cust_token is not None

    response = client.put(
        f"/requests/{mrf_id}/reject",
        headers={"Authorization": f"Bearer {cust_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["release_status"] == "Pending"

    delete_product(p1_id, admin_token)

# ==================== ADMIN TESTS ====================

def test_admin_view_all_requests():
    admin_token = login_user("peter@gmail.com", "peter")
    assert admin_token is not None

    p1_id = create_product("AdminView", admin_token=admin_token)

    tech_token = login_user("sohyun@gmail.com", "sohyun")
    assert tech_token is not None

    client.post(
        "/requests/",
        json={
            "items": [{"product_id": p1_id, "quantity": 1}],
            "mrf_files": "adminview.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    response = client.get(
        "/requests/all",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    delete_product(p1_id, admin_token)