from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.product import ProductQuery
from app.schemas.product import Product, ProductCreate
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.get("/products", response_model=Product)
def get_product(
    name: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    product_query = ProductQuery(db=db)
    return product_query.select_product(name)

@router.post("/products", response_model=Product)
def create_product(
    product: ProductCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    product_query = ProductQuery(db=db)
    return product_query.insert_product(product)

@router.put("/products", response_model=Product)
def update_product(
    name: str,
    product: ProductCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    product_query = ProductQuery(db=db)
    return product_query.update_product(name, product)

@router.delete("/products", response_model=Product)
def delete_product(
    name: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    product_query = ProductQuery(db=db)
    return product_query.delete_product(name)
