from fastapi.testclient import TestClient
from app.main import app
from app.database import sessionLocal
from app.models.user import UserManager
from app.api.products import router as products_router
from app.models.product import Product

# Force register products router
if not any(hasattr(r, "path") and r.path == "/products/" for r in app.routes):
    app.include_router(products_router)


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


# TODO: CREATE TESTS
# create products success
def test_create_product_success():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    response = client.post(
        "/products/",
        json={
            "product_name": "Docking Station",
            "product_image": "docking.jpg",
            "stock": 200
        },
        headers={"Authorization":f"Bearer {admin_token}"}

    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["product_name"] == "Docking Station"
    assert data["product_image"] == "docking.jpg"
    assert data["stock"] == 200

# create product already existing
def test_create_existing_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    product_1 = client.post(
            "/products/",
            json={
                "product_name": "USB Cable",
                "product_image": "usb.jpg",
                "stock": 100
            },
            headers={"Authorization":f"Bearer {admin_token}"}
    
        )
    
    assert product_1.status_code == 201
    data = product_1.json()
    assert "id" in data
    assert data["product_name"] == "USB Cable"
    assert data["product_image"] == "usb.jpg"
    assert data["stock"] == 100

    product_2 = client.post(
                "/products/",
                json={
                    "product_name": "USB Cable",
                    "product_image": "usb.jpg",
                    "stock": 100
                },
                headers={"Authorization":f"Bearer {admin_token}"}
        
            )
        
    assert product_2.status_code == 400
    assert "Product with this name already exists" in product_2.json()["detail"].lower()
    
def test_create_product_fail():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    response = client.post(
        "/products/",
        json={
            "product_name": "",
            "product_image": "docking.jpg",
            "stock": 200
        },
        headers={"Authorization":f"Bearer {admin_token}"}

    )

    assert response.status_code == 422
    data = response.json()
    assert "product_name" in str(data).lower()
    

# create product as non-admin
def test_create_product_as_non_admin():
    technician_token = login_user("hayeon@gmail.com", "hayeon")

    response = client.post(
            "/products/",
            json={
                "product_name": "Adaptor",
                "product_image": "adaptor.jpg",
                "stock": 200
            },
            headers={"Authorization":f"Bearer {technician_token}"}
    
        )
    
    assert response.status_code == 403


# TODO: UPDATE TESTS
# update product details

def test_update_product_success():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    product_to_update = client.post(
        "/products/",
        json={
            "product_name": "Wireless Mouse",
            "product_image": "wireless.jpg",
            "stock": 200
        },
        headers={"Authorization":f"Bearer {admin_token}"}

    )
    product_data = product_to_update.json()
    product_id = product_data["id"]

    update = client.put(
        f"/products/{product_id}",
        json={
                "product_name": "Wireless Mouse --EDITED",
                "product_image": "wireless.jpg",
                "stock": 200
        },
        headers={"Authorization":f"Bearer {admin_token}"}
    )

    assert update.status_code == 200
    data = update.json()
    assert data["product_name"] == "Wireless Mouse --EDITED"
    
# update product not existing
def test_update_nonexistent_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")


    product_id = 999 # this id doesn't exist
  
    update = client.put(
            f"/products/{product_id}",
            json={
                    "product_name": "Wireless Keyboard --EDITED",
                    "product_image": "wireless.jpg",
                    "stock": 200
            },
            headers={"Authorization":f"Bearer {admin_token}"}
        )
    
    assert update.status_code == 404
    assert "Product with this ID does not exist" in update.json()["detail"].lower()

# update product as non-admin
def test_update_product_as_non_admin():
    technician_token = login_user("hayeon@gmail.com", "hayeon")
    product_to_update = client.post(
        "/products/",
        json={
            "product_name": "Wireless Mouse",
            "product_image": "wireless.jpg",
            "stock": 200
        },
        headers={"Authorization":f"Bearer {technician_token}"}

    )
    product_data = product_to_update.json()
    product_id = product_data["id"]

    update = client.put(
            f"/products/{product_id}",
            json={
                    "product_name": "Wireless Mouse --EDITED",
                    "product_image": "wireless.jpg",
                    "stock": 200
            },
            headers={"Authorization":f"Bearer {technician_token}"}
        )

    assert update.status_code == 403


# TODO: DELETE TESTS
# delete product
def test_delete_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    response = client.post(
            "/products/",
            json={
                "product_name": "ASUS Laptop",
                "product_image": "asus.jpg",
                "stock": 200
            },
            headers={"Authorization":f"Bearer {admin_token}"}
    
        )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["product_name"] == "ASUS Laptop"
    assert data["product_image"] == "asus.jpg"
    assert data["stock"] == 200

    product_id = data["id"]

    delete = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert delete.status_code == 200

    get_resp = client.get(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_resp.status_code == 404


# delete product not existing
def test_delete_nonexistent_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")
   
    product_id = 800

    delete = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert delete.status_code == 404
    

# TODO: GET TESTS
# get all products 
def test_get_all_products():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    products = client.get(
        "/products/",
        headers={"Authorization":f"Bearer {admin_token}"}
    )

    assert products.status_code == 200

# get all products as non-admin

def test_get_all_products_as_non_admin():
    technician_token = login_user("hayeon@gmail.com", "hayeon")

    products = client.get(
        "/products/",
        headers={"Authorization":f"Bearer {technician_token}"}
    )

    assert products.status_code == 200
    assert isinstance(products.json(), list)


# get all products no auth 
def test_get_all_products_no_auth():

    products = client.get(
        "/products/",
    )
    
    assert products.status_code == 401
    assert products.json()["detail"] == "Not authenticated"


# get product by id
def test_get_product_by_id():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    response = client.post(
            "/products/",
            json={
                "product_name": "DELL Laptop",
                "product_image": "dell.jpg",
                "stock": 200
            },
            headers={"Authorization":f"Bearer {admin_token}"}
        
            )
        
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["product_name"] == "DELL Laptop"
    assert data["product_image"] == "dell.jpg"
    assert data["stock"] == 200

    product_id = data["id"]

    product = client.get(
        f"/products/{product_id}",
        headers={"Authorization":f"Bearer {admin_token}"}
    )

    assert product.status_code == 200
    assert "id" in product.json()

# get nonexistent product
def test_get_nonexistent_product():
    admin_token = login_user("nakyoung@gmail.com", "nakyoung")

    product_id = 700
    
    product = client.get(
            f"/products/{product_id}",
            headers={"Authorization":f"Bearer {admin_token}"}
        )
    
    assert product.status_code == 404

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