# API Products

API RESTful para gerenciamento de produtos com autenticação JWT, desenvolvida com FastAPI e PostgreSQL.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados
- **JWT** - Autenticação via tokens
- **Poetry** - Gerenciamento de dependências
- **Pytest** - Framework de testes

## 📋 Pré-requisitos

- Python 3.13+
- Poetry
- PostgreSQL 12+

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd api-products
```

2. Instale as dependências:
```bash
poetry install
```

3. Instale as dependências de desenvolvimento:
```bash
poetry install --with dev
```

## ⚙️ Configuração

1. Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua_chave_secreta_aqui
SQLALCHEMY_DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```

2. Configure o banco de dados PostgreSQL. Execute o seguinte SQL:
```sql
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TABLE products (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL,
    amount INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_products_modtime
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE PROCEDURE update_modified_column();
```

## 🏃 Executando a aplicação

```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa (Swagger): `http://localhost:8000/api/v1/openapi.json`
Documentação alternativa (ReDoc): `http://localhost:8000/docs`

## 📚 Endpoints

### Autenticação

#### POST `/api/v1/auth`
Autentica um usuário e retorna um token JWT.

**Body (form-data):**
- `username`: string
- `password`: string

**Resposta:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer"
}
```

### Produtos

Todos os endpoints de produtos requerem autenticação via Bearer Token.

#### GET `/api/v1/products`
Lista todos os produtos.

**Headers:**
```
Authorization: Bearer {token}
```

**Resposta:**
```json
[
    {
        "id": "uuid",
        "name": "Produto Teste",
        "category": "Categoria Teste",
        "price": 99.99,
        "amount": 10,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": "uuid",
        "name": "Produto Teste 2",
        "category": "Categoria Teste",
        "price": 199.99,
        "amount": 5,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]
```

#### GET `/api/v1/products/{name}`
Busca um produto pelo nome.

**Headers:**
```
Authorization: Bearer {token}
```

**Path Parameters:**
- `name`: string (nome do produto)

**Resposta:**
```json
{
    "id": "uuid",
    "name": "Produto Teste",
    "category": "Categoria Teste",
    "price": 99.99,
    "amount": 10,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

#### POST `/api/v1/products`
Cria um novo produto.

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
    "name": "Produto Teste",
    "category": "Categoria Teste",
    "price": 99.99,
    "amount": 10
}
```

**Validações:**
- `name`: obrigatório, mínimo 1 caractere, máximo 50 caracteres
- `category`: obrigatório, mínimo 1 caractere, máximo 50 caracteres
- `price`: obrigatório, deve ser maior que zero
- `amount`: obrigatório, deve ser maior ou igual a zero

#### PUT `/api/v1/products?name={nome}`
Atualiza um produto existente.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `name`: string (nome do produto a ser atualizado)

**Body:**
```json
{
    "name": "Produto Atualizado",
    "category": "Nova Categoria",
    "price": 149.99,
    "amount": 20
}
```

#### DELETE `/api/v1/products?name={nome}`
Remove um produto.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `name`: string (nome do produto a ser removido)

## 🧪 Testes

Execute os testes com:
```bash
poetry run pytest
```

Para executar com mais detalhes:
```bash
poetry run pytest -v
```

Para executar um arquivo específico:
```bash
poetry run pytest tests/test_products.py
```

## 📁 Estrutura do Projeto

```
api-products/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependências (get_db, get_current_user)
│   │   └── v1/
│   │       ├── api.py            # Router principal da API v1
│   │       └── endpoints/
│   │           ├── auth.py       # Endpoints de autenticação
│   │           └── products.py   # Endpoints de produtos
│   ├── core/
│   │   ├── config.py             # Configurações da aplicação
│   │   └── security.py           # Funções de segurança (JWT, hash)
│   ├── db/
│   │   └── session.py            # Configuração do banco de dados
│   ├── models/
│   │   ├── product.py            # Modelo SQLAlchemy de Product
│   │   └── user.py               # Modelo SQLAlchemy de User
│   ├── schemas/
│   │   ├── product.py            # Schemas Pydantic de Product
│   │   ├── token.py              # Schemas Pydantic de Token
│   │   └── user.py               # Schemas Pydantic de User
│   ├── services/
│   │   └── product.py            # Lógica de negócio (CRUD de produtos)
│   └── main.py                   # Aplicação FastAPI principal
├── tests/
│   ├── conftest.py               # Fixtures compartilhadas
│   ├── test_auth.py              # Testes de autenticação
│   └── test_products.py          # Testes de produtos
├── .github/
│   └── workflows/
│       ├── api-pipeline-ci.yml   # Pipeline de CI (testes em PR)
│       └── deploy.yml            # Pipeline de CD (deploy automático)
├── Dockerfile
├── pyproject.toml                # Dependências e configurações
└── README.md
```

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas:

- **Models**: Definição dos modelos SQLAlchemy (tabelas do banco)
- **Schemas**: Validação e serialização com Pydantic
- **Services**: Lógica de negócio e acesso a dados
- **Endpoints**: Rotas HTTP e validação de entrada
- **Core**: Configurações e utilitários (segurança, config)

## 🔐 Autenticação

A API utiliza autenticação JWT (JSON Web Tokens). Para acessar os endpoints protegidos:

1. Faça login em `/api/v1/auth` com suas credenciais
2. Use o token retornado no header `Authorization: Bearer {token}`
3. O token expira em 30 minutos (configurável)

## 🔄 CI/CD - GitHub Actions

O projeto possui pipelines automatizadas para integração e deploy contínuo:

### Pipeline CI (Continuous Integration)
**Arquivo:** `.github/workflows/api-pipeline-ci.yml`

Executa automaticamente em Pull Requests para a branch `main`:
- Instala Python 3.13
- Instala dependências com Poetry
- Executa todos os testes com pytest
- Valida o código antes do merge

### Pipeline CD (Continuous Deployment)
**Arquivo:** `.github/workflows/deploy.yml`

Executa automaticamente em push para a branch `main`:
- Faz login no Azure via OIDC
- Constrói a imagem Docker
- Faz push da imagem para Azure Container Registry (ACR)
- Faz deploy automático para Azure Container Apps

**Secrets necessários no GitHub:**
- `SECRET_KEY`: Chave secreta para JWT
- `SQLALCHEMY_DATABASE_URL`: URL de conexão do banco
- `AZURE_CLIENT_ID`: ID do cliente Azure
- `AZURE_TENANT_ID`: ID do tenant Azure
- `AZURE_SUBSCRIPTION_ID`: ID da subscription Azure

## 📝 Notas

- Os campos `id`, `created_at` e `updated_at` são gerados automaticamente pelo PostgreSQL
- O campo `updated_at` é atualizado automaticamente via trigger no banco de dados
- Todos os endpoints de produtos requerem autenticação
- A busca de produtos é feita pelo campo `name`

## 👤 Autor

Gustavo Moreira - moreiragustavo221@gmail.com

## 📄 Licença

Este projeto está sob a licença especificada no arquivo LICENSE.
