
# * FastAPI 
from fastapi import FastAPI, Depends, Request
from slowapi import _rate_limit_exceeded_handler

# * Rate Limiting
from slowapi.errors import RateLimitExceeded
from app.utils.rate_limit import limiter
from fastapi.middleware.cors import CORSMiddleware

# * Modules
from app.database import engine, Base
from app.api import auth_router, products_router, material_request_router, inventory_router





# FastAPI itself
app = FastAPI(
    title="Inventory Management System API",
    version="0.1.0",
    description="API for managing inventory, requests, and approvals"
)

# * Creating the rate limiter
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


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
app.include_router(inventory_router)

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