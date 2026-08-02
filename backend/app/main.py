from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models.user import UserManager
from app.api import auth_router, products_router, material_request_router
from app.database import get_db

app = FastAPI(
    title="Inventory Management System API",
    version="0.1.0",
    description="API for managing inventory, requests, and approvals"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Create all tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(material_request_router)

@app.get("/")
async def root():
    return {
        "message": "Inventory Management System API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}