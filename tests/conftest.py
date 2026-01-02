import pytest
import uuid
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.pool import StaticPool

# Importa módulos ANTES de definir os modelos de teste
import app.models.product as product_module
import app.models.user as user_module
import app.services.product as service_module

from app.core import security
from app.api import deps


# Base separada para testes
class TestBase(DeclarativeBase):
    pass


class UserTest(TestBase):
    """Modelo de usuário para testes."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class ProductTest(TestBase):
    """Modelo de produto para testes (compatível com SQLite)."""
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    name = Column(String(50), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    amount = Column(Integer, nullable=False, index=True)
    
    def __init__(self, **kwargs):
        if "id" not in kwargs:
            kwargs["id"] = str(uuid.uuid4())
        if "created_at" not in kwargs:
            kwargs["created_at"] = datetime.now(timezone.utc)
        if "updated_at" not in kwargs:
            kwargs["updated_at"] = datetime.now(timezone.utc)
        super().__init__(**kwargs)


# Faz monkeypatch dos modelos ANTES de importar app.main
product_module.Product = ProductTest
user_module.User = UserTest
service_module.ProductModel = ProductTest

# Agora importa app.main (que já usará os modelos mockados)
from app.main import app


@pytest.fixture(scope="function")
def db_session():
    # Cria um banco único em memória para cada teste
    # Cada teste terá seu próprio banco isolado
    db_url = "sqlite:///:memory:"
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    TestBase.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        TestBase.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture(scope="function")
def test_user(db_session: Session):
    # Verifica se o usuário já existe antes de criar
    existing_user = db_session.query(UserTest).filter(UserTest.username == "testuser").first()
    if existing_user:
        return existing_user
    
    hashed_password = security.get_password_hash("testpassword")
    user = UserTest(username="testuser", hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def client(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[deps.get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def authenticated_client(db_session: Session, test_user):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_current_user():
        return test_user

    app.dependency_overrides[deps.get_db] = override_get_db
    app.dependency_overrides[deps.get_current_user] = override_get_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(test_user):
    from app.core import security
    from app.core.config import settings
    from datetime import timedelta

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(test_user.id, expires_delta=access_token_expires)
    return token




@pytest.fixture
def sample_product_data():
    return {
        "name": "Produto Teste",
        "category": "Categoria Teste",
        "price": 99.99,
        "amount": 10
    }
