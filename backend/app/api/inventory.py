from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models.inventory import ProductsInventory, AreaEnum
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    AddStockResponse,
    TotalStockResponse,
    ProductStockByArea,
    InventorySummaryResponse,
    AreaSummary,
    StockHistoryResponse
)
from app.utils.auth import get_current_admin
from app.models.product import Product
from app.models.stock import Stock
from app.models.logs import Log

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.utils.database import db_dependency
from app.models.user import UserManager

from app.utils.rate_limit import rate_limit

router = APIRouter(prefix="/inventory", tags=["Products Inventory"])


@router.post("/add", response_model=AddStockResponse, status_code=status.HTTP_201_CREATED)
@rate_limit(10)
def add_stock(
    request: Request,
    data: InventoryCreate,
    db: Session = db_dependency,
    current_user: UserManager = Depends(get_current_admin)
):
    # check if product exists
    product = db.query(Product).filter(
        Product.id == data.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    areas = [area.value for area in AreaEnum]
    if data.area not in areas:
        raise HTTPException(status_code=400, detail=f"invalid area")


    # add product
    inventory = db.query(ProductsInventory).filter(
        ProductsInventory.product_id == data.product_id,
        ProductsInventory.area == data.area
    ).first()

    if not inventory:
        inventory = ProductsInventory(
            product_id = data.product_id,
            stock = data.quantity,
            area = data.area
        )
        db.add(inventory)
        db.flush()
    else:
        inventory.stock += data.quantity


    # add to logs table
    log_entry = Log(
        wh_email=current_user.email,
        wh_proof=data.wh_proof
    )
    db.add(log_entry)
    db.flush()

    # add to add_stock table

    stock_entry = Stock(
        inventory_id=inventory.id,
        quantity=data.quantity,
        wh_id=current_user.email,
        wh_logs=log_entry.id
    )
    db.add(stock_entry)

    db.commit()

    # return
    return {
        "add_id": stock_entry.id,
        "product_id": data.product_id,
        "area": data.area,
        "quantity": data.quantity,
        "wh_id": current_user.email,
        "new_stock": inventory.stock
    }


@router.get("/area/{area}", response_model=List[InventoryResponse])
def get_stock_by_area(
    area: AreaEnum,
    db: Session = db_dependency,
    current_user = Depends(get_current_admin)
):
    inventory = db.query(ProductsInventory).join(Product).filter(
        ProductsInventory.area == area
    ).all()

    return [
        {
            "id": i.id,
            "product_id": i.product_id,
            "product_name": i.product.product_name,
            "area": i.area,
            "stock": i.stock
        }
        for i in inventory
    ]


@router.get("/all", response_model=List[InventoryResponse], status_code=status.HTTP_200_OK)
def get_all_inventory(
    db: Session = db_dependency,
    current_user = Depends(get_current_admin)
):
    all_inventory = db.query(ProductsInventory).join(Product).all()

    return [
        {
            "id": i.id,
            "product_id": i.product_id,
            "product_name": i.product.product_name,
            "area": i.area,
            "stock": i.stock
        }
        for i in all_inventory
    ]


# total of specific product
@router.get("/total/{product_id}", response_model=TotalStockResponse, status_code=status.HTTP_200_OK)
def get_total_of_product(
    product_id: int,
    db: Session = db_dependency,
    current_user = Depends(get_current_admin)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    total = db.query(func.sum(ProductsInventory.stock)).filter(
        ProductsInventory.product_id == product_id
    ).scalar() or 0

    return {
        "product_id": product_id,
        "product_name": product.product_name,
        "total_stock": total
    }

@router.get("/product/{product_id}", response_model=ProductStockByArea, status_code=status.HTTP_200_OK)
def get_stock_by_product(
    product_id: int,
    db: Session = db_dependency,
    current_user = Depends(get_current_admin)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found") 

    inventory = db.query(ProductsInventory).filter(
        ProductsInventory.product_id == product_id
    ).all()

    return {
        "product_id": product_id,
        "product_name": product.product_name,
        "areas": [
            {"area": i.area, "stock": i.stock}
            for i in inventory
        ]
    }

@router.get("/summary", response_model=InventorySummaryResponse, status_code=status.HTTP_200_OK)
def get_summary(
    db: Session = db_dependency,
    current_user = Depends(get_current_admin)
):
    summary = db.query(
        ProductsInventory.area,
        func.sum(ProductsInventory.stock).label("total_stock"),
        func.count(ProductsInventory.id).label("product_count")
    ).group_by(ProductsInventory.area).all()

    total = db.query(func.sum(ProductsInventory.stock)).scalar() or 0

    return {
        "grand_total": total,
        "per_area": [
            AreaSummary(
                area=row.area,
                total_stock=row.total_stock or 0,
                product_count=row.product_count or 0
            )
            for row in summary
        ]
    }

@router.get("/history", response_model=List[StockHistoryResponse])
def get_stock_history(
    db: Session = db_dependency,
    current_user = Depends(get_current_admin)
):
    history = db.query(Stock).join(ProductsInventory).join(Product).join(Log).all()

    return [
        {
            "add_id": entry.id,
            "product_name": entry.inventory.product.product_name,
            "area": entry.inventory.area,
            "quantity": entry.quantity,
            "wh_id": entry.wh_id,
            "date": entry.date,
            "wh_proof": entry.log_entry.wh_proof
        }
        for entry in history
    ]
