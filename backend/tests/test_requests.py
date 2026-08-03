from fastapi.testclient import TestClient
from app.main import app
from app.database import sessionLocal
from app.models.user import UserManager
from app.api.material_request import router as material_request_router


if not any(hasattr(r,'path') and r.path == "/requests/" for r in app.routes):
    app.include_router(material_request_router)



client = TestClient(app)



# ==================== HELPER FUNCTIONS ====================

def create_test_user(role: str, email: str, password: str):
    """Helper to create test users with different roles"""
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
    """Helper to login and get token"""
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password
        }
    )
    return response.json().get("access_token")


# ==================== SETUP ====================

def setup_module(module):
    """Setup test data before running tests"""
    print("=== SETUP IS RUNNING ===")
    
    # Create users
    create_test_user("Admin", "peter@gmail.com", "peter")
    create_test_user("Technician", "sohyun@gmail.com", "sohyun")
    create_test_user("Supervisor", "hina@gmail.com", "hina")
    create_test_user("Custodian", "steve@gmail.com", "steve")
    
    # Create products with explicit wait for database
    

    print("=== SETUP IS COMPLETE ===")


# ==================== TECHNICIAN TESTS ====================

def test_technician_create_request():
    token = login_user("sohyun@gmail.com", "sohyun")

    admin_token = login_user("peter@gmail.com", "peter")

    product_1 = client.post(
        "/products/",
        json={"product_name": "Test Mouse", "product_image": "laptop.jpg", "stock": 200},  
        headers={"Authorization": f"Bearer {admin_token}"}
        )
    assert product_1.status_code == 201, f"Failed to create Mouse: {product_1.json()}"
    
    product_2 = client.post(
            "/products/",
            json={"product_name": "Test Mousepad", "product_image": "mouse.jpg", "stock": 200},  
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    assert product_2.status_code == 201, f"Failed to create Mousepad: {product_2.json()}"

    product1 = product_1.json()
    product1_id = product1["id"]

    product2 = product_1.json()
    product2_id = product2["id"]
    
    response = client.post(
        "/requests/",
        json={
            "items": [
                {"product_id": product1_id, "quantity": 2},
                {"product_id": product2_id, "quantity": 3}
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

def test_technician_create_request_invalid_product():
    token = login_user("sohyun@gmail.com", "sohyun")
    
    response = client.post(
        "/requests/",
        json={
            "items": [
                {"product_id": 999, "quantity": 2}
            ],
            "mrf_files": "photo.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_technician_view_my_requests():
    token = login_user("sohyun@gmail.com", "sohyun")
    
    response = client.get(
        "/requests/sent",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# ==================== SUPERVISOR TESTS ====================

def test_supervisor_view_pending():
    token = login_user("hina@gmail.com", "hina")
    
    response = client.get(
        "/requests/pending",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_supervisor_approve_request():
    # First create a request as technician
    tech_token = login_user("sohyun@gmail.com", "sohyun")
    create_response = client.post(
        "/requests/",
        json={
            "items": [{"product_id": 1, "quantity": 2}],
            "mrf_files": "photo.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    mrf_id = create_response.json()["mrf_id"]
    
    # Supervisor approves
    sup_token = login_user("hina@gmail.com", "hina")
    response = client.put(
        f"/requests/{mrf_id}/approve",
        headers={"Authorization": f"Bearer {sup_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["approval_status"] == "Approved"
    assert data["approved_by"] == "hina@gmail.com"

def test_supervisor_disapprove_request():
    # Create a request
    tech_token = login_user("sohyun@gmail.com", "sohyun")
    create_response = client.post(
        "/requests/",
        json={
            "items": [{"product_id": 2, "quantity": 3}],
            "mrf_files": "photo.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    mrf_id = create_response.json()["mrf_id"]
    
    # Supervisor disapproves
    sup_token = login_user("hina@gmail.com", "hina")
    response = client.put(
        f"/requests/{mrf_id}/disapprove",
        headers={"Authorization": f"Bearer {sup_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["approval_status"] == "Not Approved"

def test_supervisor_edit_request():
    # Create a request
    tech_token = login_user("sohyun@gmail.com", "sohyun")
    create_response = client.post(
        "/requests/",
        json={
            "items": [{"product_id": 1, "quantity": 2}],
            "mrf_files": "photo.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    mrf_id = create_response.json()["mrf_id"]
    
    # Supervisor edits
    sup_token = login_user("hina@gmail.com", "hina")
    response = client.put(
        f"/requests/{mrf_id}/edit",
        json=[
            {"product_id": 1, "quantity": 5},
            {"product_id": 2, "quantity": 3}
        ],
        headers={"Authorization": f"Bearer {sup_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    # Check quantities
    for item in data["items"]:
        if item["product_id"] == 1:
            assert item["quantity"] == 5


# ==================== CUSTODIAN TESTS ====================

def test_custodian_view_approved_requests():
    token = login_user("steve@gmail.com", "steve")
    
    response = client.get(
        "/requests/approved",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_custodian_release_request():
    # Create a request
    tech_token = login_user("sohyun@gmail.com", "sohyun")
    create_response = client.post(
        "/requests/",
        json={
            "items": [{"product_id": 1, "quantity": 2}],
            "mrf_files": "photo.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    mrf_id = create_response.json()["mrf_id"]
    
    # Supervisor approves
    sup_token = login_user("hina@gmail.com", "hina")
    client.put(
        f"/requests/{mrf_id}/approve",
        headers={"Authorization": f"Bearer {sup_token}"}
    )
    
    # Custodian releases
    cust_token = login_user("steve@gmail.com", "steve")
    response = client.put(
        f"/requests/{mrf_id}/release",
        headers={"Authorization": f"Bearer {cust_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["release_status"] == "Released"
    assert data["released_by"] == "steve@gmail.com"

def test_custodian_reject_request():
    # Create a request
    tech_token = login_user("sohyun@gmail.com", "sohyun")
    create_response = client.post(
        "/requests/",
        json={
            "items": [{"product_id": 2, "quantity": 3}],
            "mrf_files": "photo.jpg"
        },
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    mrf_id = create_response.json()["mrf_id"]
    
    # Supervisor approves
    sup_token = login_user("hina@gmail.com", "hina")
    client.put(
        f"/requests/{mrf_id}/approve",
        headers={"Authorization": f"Bearer {sup_token}"}
    )
    
    # Custodian rejects
    cust_token = login_user("steve@gmail.com", "steve")
    response = client.put(
        f"/requests/{mrf_id}/reject",
        headers={"Authorization": f"Bearer {cust_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["release_status"] == "Pending"


# ==================== ADMIN TESTS ====================

def test_admin_view_all_requests():
    token = login_user("peter@gmail.com", "peter")
    
    response = client.get(
        "/requests/all",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)