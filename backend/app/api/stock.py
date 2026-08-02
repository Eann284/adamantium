from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.database import db_dependency

from app.models.user import UserManager
from app.models.product import Product
from app.models.stock import Stock
from app.models.logs import Log
from app.schemas.stock import StockResponse, StockCreate
from app.schemas.logs import LogResponse, LogCreate

from app.utils.auth import get_current_admin


router = APIRouter(prefix="/stock", tags=["Add Stock"])

# admin adds stock to existing product in products table
# auto adds a log entry as well

@router.post("/", response_model=StockResponse, status_code=status.HTTP_201_CREATED)
def add_stock(
    stock: StockCreate,
    db:Session = db_dependency,
    current_user = Depends(get_current_admin)
    ):

    product = db.query(Product).filter(Product.id == stock.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # auto log entry
    new_log = Log(
        wh_email = current_user.email,
        wh_proof = stock.wh_proof or None
    )

    db.add(new_log)
    db.flush()

    # add the stock
    new_stock = Stock(
        wh_id = current_user.email,
        wh_logs = new_log.id,
        product_id = stock.product_id,
        quantity = stock.quantity
    )

    db.add(new_stock)

    # update products table
    product.stock = stock.quantity

    db.commit()
    db.refresh(new_stock)

    # return
    return new_stock


@router.get("/logs", response_model=List[LogResponse], status_code=status.HTTP_200_OK)
def get_logs(db: Session = db_dependency, current_user = Depends(get_current_admin), skip:int = 0, limit:int = 10):
    logs = db.query(Log).order_by(Log.date.desc()).offset(skip).limit(limit).all()

    return logs

@router.get("/", response_model=List[dict])
def get_stocks(db:Session = db_dependency, current_user:UserManager = Depends(get_current_admin)):

    products = db.query(Product).all()

    return [
        {
            "id": product.id,
            "product_name": product.product_name,
            "stock": product.stock

        }
        for product in products
    ]
