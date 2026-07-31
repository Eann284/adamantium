from app.api.auth import router as auth_router
from app.api.products import router as products_router
from app.api.material_request import router as material_request_router

__all__ = [
    "auth_router",
    "products_router",
    "material_request_router"
]