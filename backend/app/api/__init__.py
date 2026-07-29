from app.api.auth import router as auth_router
from app.api.products import router as products_router

__all__ = [
    "auth_router",
    "products_router"
]