from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Nome do produto (máximo 50 caracteres)")
    category: str = Field(..., min_length=1, max_length=50, description="Categoria do produto (máximo 50 caracteres)")
    price: float = Field(..., gt=0, description="Preço do produto (deve ser maior que zero)")
    amount: int = Field(..., ge=0, description="Quantidade em estoque (deve ser maior ou igual a zero)")

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)