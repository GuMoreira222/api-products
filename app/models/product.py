from sqlalchemy import Column, Integer, String, Float, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    # Campos gerados pelo PostgreSQL (DEFAULT e TRIGGER)
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    
    # Campos da aplicação
    name = Column(String(50), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    amount = Column(Integer, nullable=False, index=True)
