from app.schemas.product import Product, ProductCreate
from app.models.product import Product as ProductModel
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class ProductQuery:
    def __init__(self, db: Session):
        self.db = db

    def select_product(self, name: str) -> Product:
        product_model = self.db.query(ProductModel).filter(ProductModel.name == name).first()
        if not product_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product_model

    def insert_product(self, product: ProductCreate) -> Product:
        try:
            product_model = ProductModel(
                name=product.name,
                category=product.category,
                price=product.price,
                amount=product.amount
            )
            self.db.add(product_model)
            self.db.commit()
            self.db.refresh(product_model)
            return product_model
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    def update_product(self, name: str, product: ProductCreate) -> Product:
        product_model = self.db.query(ProductModel).filter(ProductModel.name == name).first()
        if not product_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")       
        try:
            product_model.name = product.name
            product_model.category = product.category
            product_model.price = product.price
            product_model.amount = product.amount
            self.db.commit()
            self.db.refresh(product_model)
            return product_model
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    def delete_product(self, name: str) -> Product:
        product_model = self.db.query(ProductModel).filter(ProductModel.name == name).first()
        if not product_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        try:
            self.db.delete(product_model)
            self.db.commit()
            return product_model
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    def get_all_products(self) -> list[Product]:
        return self.db.query(ProductModel).all()