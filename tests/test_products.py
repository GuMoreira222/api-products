import pytest
from fastapi import status
from sqlalchemy.orm import Session

from tests.conftest import ProductTest
from app.services.product import ProductQuery
from app.schemas.product import ProductCreate


class TestProductService:
    def test_select_product_success(self, db_session: Session, sample_product_data):
        product = ProductTest(**sample_product_data)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        service = ProductQuery(db=db_session)
        result = service.select_product("Produto Teste")

        assert result.name == "Produto Teste"
        assert result.category == "Categoria Teste"
        assert result.price == 99.99
        assert result.amount == 10

    def test_select_product_not_found(self, db_session: Session):
        service = ProductQuery(db=db_session)
        
        with pytest.raises(Exception) as exc_info:
            service.select_product("Produto Inexistente")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

    def test_insert_product_success(self, db_session: Session, sample_product_data):
        service = ProductQuery(db=db_session)
        product_create = ProductCreate(**sample_product_data)
        
        result = service.insert_product(product_create)

        assert result.name == "Produto Teste"
        assert result.category == "Categoria Teste"
        assert result.price == 99.99
        assert result.amount == 10
        assert result.id is not None
        assert hasattr(result, "created_at")

    def test_update_product_success(self, db_session: Session, sample_product_data):
        product = ProductTest(**sample_product_data)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        service = ProductQuery(db=db_session)
        updated_data = {
            "name": "Produto Atualizado",
            "category": "Nova Categoria",
            "price": 149.99,
            "amount": 20
        }
        product_update = ProductCreate(**updated_data)
        
        result = service.update_product("Produto Teste", product_update)

        assert result.name == "Produto Atualizado"
        assert result.category == "Nova Categoria"
        assert result.price == 149.99
        assert result.amount == 20

    def test_update_product_not_found(self, db_session: Session, sample_product_data):
        service = ProductQuery(db=db_session)
        product_update = ProductCreate(**sample_product_data)
        
        with pytest.raises(Exception) as exc_info:
            service.update_product("Produto Inexistente", product_update)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_success(self, db_session: Session, sample_product_data):
        product = ProductTest(**sample_product_data)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        service = ProductQuery(db=db_session)
        result = service.delete_product("Produto Teste")

        assert result.name == "Produto Teste"
        
        # Verifica se o produto foi realmente deletado
        db_session.expire_all()  # Limpa cache da sessão
        deleted = db_session.query(ProductTest).filter(ProductTest.name == "Produto Teste").first()
        assert deleted is None

    def test_delete_product_not_found(self, db_session: Session):
        service = ProductQuery(db=db_session)
        
        with pytest.raises(Exception) as exc_info:
            service.delete_product("Produto Inexistente")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


class TestProductEndpoints:
    def test_get_product_success(self, authenticated_client, db_session: Session, sample_product_data):
        product = ProductTest(**sample_product_data)
        db_session.add(product)
        db_session.commit()

        response = authenticated_client.get("/api/v1/products?name=Produto Teste")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Produto Teste"
        assert data["category"] == "Categoria Teste"
        assert data["price"] == 99.99
        assert data["amount"] == 10

    def test_get_product_not_found(self, authenticated_client):
        response = authenticated_client.get("/api/v1/products?name=Produto Inexistente")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_product_unauthorized(self, client):
        response = client.get("/api/v1/products?name=Produto Teste")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_product_success(self, authenticated_client, sample_product_data):
        response = authenticated_client.post("/api/v1/products", json=sample_product_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Produto Teste"
        assert data["category"] == "Categoria Teste"
        assert data["price"] == 99.99
        assert data["amount"] == 10
        assert "id" in data
        assert "created_at" in data

    def test_create_product_unauthorized(self, client, sample_product_data):
        response = client.post("/api/v1/products", json=sample_product_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_product_invalid_data(self, authenticated_client):
        invalid_data = {
            "name": "",
            "category": "Categoria",
            "price": -10,
            "amount": -5
        }
        response = authenticated_client.post("/api/v1/products", json=invalid_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_update_product_success(self, authenticated_client, db_session: Session, sample_product_data):
        product = ProductTest(**sample_product_data)
        db_session.add(product)
        db_session.commit()

        updated_data = {
            "name": "Produto Atualizado",
            "category": "Nova Categoria",
            "price": 149.99,
            "amount": 20
        }
        response = authenticated_client.put("/api/v1/products?name=Produto Teste", json=updated_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Produto Atualizado"
        assert data["category"] == "Nova Categoria"
        assert data["price"] == 149.99
        assert data["amount"] == 20

    def test_update_product_not_found(self, authenticated_client, sample_product_data):
        response = authenticated_client.put("/api/v1/products?name=Produto Inexistente", json=sample_product_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_success(self, authenticated_client, db_session: Session, sample_product_data):
        product = ProductTest(**sample_product_data)
        db_session.add(product)
        db_session.commit()

        response = authenticated_client.delete("/api/v1/products?name=Produto Teste")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Produto Teste"

    def test_delete_product_not_found(self, authenticated_client):
        response = authenticated_client.delete("/api/v1/products?name=Produto Inexistente")

        assert response.status_code == status.HTTP_404_NOT_FOUND

