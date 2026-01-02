# Testes da API Products

## Estrutura de Testes

- `conftest.py`: Fixtures compartilhadas (cliente HTTP, sessão de banco, usuário de teste, etc.)
- `test_products.py`: Testes dos endpoints e services de produtos
- `test_auth.py`: Testes do endpoint de autenticação

## Como Executar

```bash
# Executar todos os testes
poetry run pytest

# Executar com verbose
poetry run pytest -v

# Executar um arquivo específico
poetry run pytest tests/test_products.py

# Executar uma classe específica
poetry run pytest tests/test_products.py::TestProductService

# Executar um teste específico
poetry run pytest tests/test_products.py::TestProductService::test_select_product_success
```

## Cobertura de Testes

### TestProductService
- `test_get_all_products_success`: Testa listagem de múltiplos produtos
- `test_get_all_products_empty`: Testa listagem quando não há produtos
- `test_select_product_success`: Testa busca de produto por nome
- `test_select_product_not_found`: Testa busca de produto inexistente
- `test_insert_product_success`: Testa criação de produto
- `test_update_product_success`: Testa atualização de produto
- `test_update_product_not_found`: Testa atualização de produto inexistente
- `test_delete_product_success`: Testa remoção de produto
- `test_delete_product_not_found`: Testa remoção de produto inexistente

### TestProductEndpoints
- `test_get_all_products_success`: Testa endpoint GET `/api/v1/products` (lista)
- `test_get_all_products_empty`: Testa endpoint GET `/api/v1/products` (lista vazia)
- `test_get_all_products_unauthorized`: Testa autenticação no endpoint de listagem
- `test_get_product_success`: Testa endpoint GET `/api/v1/products/{name}`
- `test_get_product_not_found`: Testa endpoint GET com produto inexistente
- `test_get_product_unauthorized`: Testa autenticação no endpoint de busca
- `test_create_product_success`: Testa endpoint POST `/api/v1/products`
- `test_create_product_unauthorized`: Testa autenticação no endpoint de criação
- `test_create_product_invalid_data`: Testa validação de dados inválidos
- `test_update_product_success`: Testa endpoint PUT `/api/v1/products`
- `test_update_product_not_found`: Testa atualização de produto inexistente
- `test_delete_product_success`: Testa endpoint DELETE `/api/v1/products`
- `test_delete_product_not_found`: Testa remoção de produto inexistente

### TestAuthEndpoint
- `test_login_success`: Testa login com credenciais válidas
- `test_login_invalid_username`: Testa login com usuário inválido
- `test_login_invalid_password`: Testa login com senha inválida
- `test_login_missing_credentials`: Testa login sem credenciais
- `test_token_validity`: Testa validade do token gerado

## Observações

- Os testes usam SQLite em memória para isolamento e performance
- Cada teste tem seu próprio banco de dados limpo
- O modelo Product é substituído por ProductTest (compatível com SQLite) durante os testes
- As dependências de autenticação são mockadas automaticamente
- Total de 22 testes cobrindo todos os endpoints e funcionalidades principais

