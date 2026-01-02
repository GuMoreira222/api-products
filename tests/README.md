# Testes da API Products

## Estrutura de Testes

- `conftest.py`: Fixtures compartilhadas (cliente HTTP, sessão de banco, usuário de teste, etc.)
- `test_products.py`: Testes dos endpoints e services de produtos
- `test_auth.py`: Testes do endpoint de autenticação

## Como Executar

```bash
# Executar todos os testes
pytest

# Executar com verbose
pytest -v

# Executar um arquivo específico
pytest tests/test_products.py

# Executar uma classe específica
pytest tests/test_products.py::TestProductService

# Executar um teste específico
pytest tests/test_products.py::TestProductService::test_select_product_success
```

## Observações

- Os testes usam SQLite em memória para isolamento
- Cada teste tem seu próprio banco de dados limpo
- O modelo Product é substituído por ProductTest (compatível com SQLite) durante os testes
- As dependências de autenticação são mockadas automaticamente

