from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.schemas.products import ProductCreate, ProductUpdate, ProductResponse
from app.utils.auth import get_current_admin
from app.utils.database import db_dependency

router = APIRouter(prefix="/products", tags=["Products"])


# get all products
@router.get("/", response_model = List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit:int = 100,
    db:Session = db_dependency
):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# get product by id
@router.get("/{product_id}", response_model = ProductResponse)
def get_product_by_id(product_id: int, db:Session = db_dependency):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


# create product
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db:Session = db_dependency, current_user = Depends(get_current_admin)):
    existing_product = db.query(Product).filter(Product.product_name == product.product_name).first()

    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists"
        )

    # creating new product
    new_product = Product(
        product_name = product.product_name,
        product_image = product.product_image
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# update product
@router.put("/{product_id}", response_model=ProductUpdate, status_code=status.HTTP_201_CREATED)
def update_product(product_id: int, product_update: ProductUpdate, db:Session = db_dependency):
    product_to_update = db.query(Product).filter(Product.id == product_id).first()
    if not product_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not Found."
        )

    if product_update.product_name is not None:
        existing_product= db.query(Product).filter(
            Product.product_name == product_update.product_name,
            Product.id != product_id
        ).first()

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists"
            )

    if product_update.Product_image is not None:
        product_to_update.Product_image = product_update.Product_image

    db.commit()
    db.refresh(product_to_update)

    return product_to_update



# delete product
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id:int, db:Session = db_dependency, current_user = Depends(get_current_admin)):
    product_to_delete = db.query(Product).filter(Product.id == product_id).first()

    if not product_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    db.delete(product_to_delete)
    db.commit()
    return None
