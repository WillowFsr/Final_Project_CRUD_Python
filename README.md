# Guia do Projeto e Fundamentos de Persistência

Documento técnico de referência sobre a estrutura atual do projeto, separação de responsabilidades, persistência com PostgreSQL, domínio, casos de uso e camada de API.

---

## Princípios de Arquitetura

O projeto procura seguir princípios de Clean Architecture e conceitos de DDD de forma pragmática.

Algumas regras adotadas:

- o domínio não deve depender de SQLAlchemy;
- a API não deve conter regras de negócio da compra;
- repositories cuidam da persistência;
- casos de uso orquestram operações de negócio;
- entities representam a persistência e o mapeamento relacional;
- regras específicas do negócio devem permanecer no domínio ou nos casos de uso, conforme sua responsabilidade.

O objetivo é manter o projeto simples o suficiente para evolução gradual, sem acoplar a regra de negócio à infraestrutura.


## 1. Visão Geral

O projeto é uma aplicação Python organizada em camadas, com foco em separação de responsabilidades e isolamento da regra de negócio em relação aos detalhes de persistência e à interface HTTP.

Atualmente, o sistema possui:

- PostgreSQL como banco de dados;
- SQLAlchemy como ORM;
- Psycopg para comunicação com PostgreSQL;
- camada de domínio para regras e entidades de negócio;
- repositories para persistência;
- casos de uso para orquestração das operações de negócio;
- início da camada HTTP com FastAPI;
- Uvicorn para execução da API.

O fluxo principal de compra já foi implementado e validado com persistência real no PostgreSQL.

---

## 2. Estrutura e Camadas do Projeto

```text
Final_Project_CRUD_Python/
├── .env                         # Variáveis de ambiente locais
├── .env.example                 # Modelo das variáveis de ambiente
├── requirements.txt             # Dependências do projeto
└── project/
    ├── __init__.py
    ├── main.py                  # Testes e ponto de entrada local
    │
    ├── api/                     # Camada HTTP / FastAPI
    │   ├── __init__.py
    │   ├── app.py               # Instância principal do FastAPI
    │   ├── routes/               # Endpoints da aplicação
    │   │   └── __init__.py
    │   └── schemas/              # Modelos Pydantic de entrada/saída
    │       └── __init__.py
    │
    ├── application/             # Casos de uso da aplicação
    │   ├── __init__.py
    │   └── use_cases/
    │       ├── __init__.py
    │       └── RealizarCompra.py
    │
    ├── domain/                  # Regras e entidades de negócio
    │   ├── Cliente.py
    │   ├── Cartao.py
    │   ├── Produto.py
    │   ├── Carrinho.py
    │   ├── ProdutoCarrinho.py
    │   └── ...
    │
    └── infra/                   # Detalhes de infraestrutura
        ├── __init__.py
        ├── configs/
        │   ├── connection.py   # Conexão e gerenciamento de sessão
        │   └── ...
        ├── entities/            # Mapeamento SQLAlchemy das tabelas
        └── repository/          # Persistência e consultas
```

### Responsabilidades das camadas

**`domain/`**

Contém os objetos e regras de negócio independentes de banco de dados ou HTTP.

**`application/use_cases/`**

Coordena operações de negócio que envolvem várias entidades e repositories. Um exemplo é o `RealizarCompra`.

**`infra/entities/`**

Contém os mapeamentos SQLAlchemy que representam as tabelas do PostgreSQL.

**`infra/repository/`**

Responsável por persistir, consultar, atualizar e remover dados do banco.

**`api/`**

Camada responsável pela comunicação HTTP. As rotas recebem as requisições, validam os dados por meio dos schemas e chamam os casos de uso ou repositories apropriados.

---

## 3. Modelo de Dados Atual

O banco possui atualmente as seguintes tabelas:

```text
cliente
├── cartao
├── carrinho
│   └── produto_carrinho ─── produto
└── historico_compra
    └── item_historico ───── produto
```

### Tabelas

- `cliente`: dados dos clientes;
- `cartao`: cartões vinculados a clientes e seus saldos;
- `produto`: produtos, preços e estoque;
- `carrinho`: carrinho persistido de cada cliente;
- `produto_carrinho`: produtos e quantidades presentes no carrinho;
- `historico_compra`: registro de cada compra realizada;
- `item_historico`: itens de cada compra, incluindo o preço praticado no momento da compra.

O banco utiliza chaves estrangeiras e `ON DELETE CASCADE` nos relacionamentos em que o ciclo de vida dos dados depende do registro pai.

---

## 4. Repositories

Os repositories fazem a ponte entre o domínio e as entities do SQLAlchemy.

Atualmente o projeto possui repositories para operações relacionadas a:

- `Cliente`;
- `Cartao`;
- `Produto`;
- `Carrinho`;
- `Historico_Compra`.

Um princípio adotado no projeto é que objetos auxiliares de relacionamento, como `ProdutoCarrinho`, não precisam necessariamente de um repository próprio quando sua persistência é responsabilidade do repository do agregado ao qual pertencem.

---
