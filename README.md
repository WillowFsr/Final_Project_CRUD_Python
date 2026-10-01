# AUREA — E-commerce em Python

> Aplicação de e-commerce desenvolvida em Python, com PostgreSQL, SQLAlchemy, FastAPI e uma interface web integrada. O projeto foi construído com foco em separação de responsabilidades, princípios de Clean Architecture e conceitos de Domain-Driven Design (DDD).

## Sobre o projeto

O AUREA é uma aplicação de loja virtual criada como projeto final de formação em programação Python.

A aplicação reúne uma camada de domínio com regras de negócio, uma camada de aplicação para os casos de uso, infraestrutura para persistência dos dados e uma API HTTP construída com FastAPI. A interface web utiliza Jinja2, HTML, CSS e JavaScript e consome a própria API do sistema.

O fluxo principal de e-commerce já foi validado com dados persistidos no PostgreSQL, incluindo cadastro de clientes, cartões, produtos, carrinho, checkout e histórico de compras.

## Principais funcionalidades

- Cadastro, consulta, atualização e exclusão de clientes.
- Cadastro, consulta, atualização e exclusão de produtos.
- Controle de estoque e preço dos produtos.
- Cadastro de cartões vinculados aos clientes.
- Controle de saldo dos cartões.
- Carrinho persistido por cliente.
- Adição de produtos ao carrinho.
- Acúmulo de quantidade quando o mesmo produto é adicionado novamente.
- Remoção de produtos do carrinho.
- Cálculo automático do total da compra.
- Checkout com validação de saldo e estoque.
- Atualização do saldo do cartão após a compra.
- Atualização do estoque após a compra.
- Limpeza do carrinho após uma compra concluída.
- Registro do histórico da compra.
- Registro do preço do produto no momento da compra (`preco_momento`).
- Interface web para navegação da loja, conta, sacola, checkout e histórico.
- Área de gestão para cadastro e manutenção de produtos.
- Documentação interativa da API com Swagger/OpenAPI.

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| FastAPI | API HTTP |
| Uvicorn | Servidor ASGI |
| Pydantic | Validação e schemas da API |
| SQLAlchemy | ORM e mapeamento relacional |
| Psycopg | Comunicação com PostgreSQL |
| PostgreSQL | Banco de dados |
| Jinja2 | Templates HTML |
| HTML / CSS / JavaScript | Interface web |
| Clean Architecture | Organização das responsabilidades |
| DDD | Modelagem e regras do domínio |

## Arquitetura

A estrutura do projeto busca manter o domínio independente dos detalhes de infraestrutura e da camada HTTP.

```text
project/
├── api/
│   ├── app.py
│   ├── routes/
│   ├── schemas/
│   └── templates/
│       ├── pages/
│       └── static/
│           ├── css/
│           └── js/
│
├── application/
│   └── use_cases/
│       └── RealizarCompra.py
│
├── domain/
│   ├── Cliente.py
│   ├── Cartao.py
│   ├── Produto.py
│   ├── Carrinho.py
│   └── ProdutoCarrinho.py
│
└── infra/
    ├── configs/
    ├── entities/
    └── repository/
```

### Responsabilidade das camadas

**Domain**

Concentra entidades e regras de negócio, evitando dependência direta de FastAPI, SQLAlchemy ou PostgreSQL.

**Application**

Orquestra operações de negócio que envolvem múltiplas entidades e componentes. O principal exemplo é o caso de uso `RealizarCompra`.

**Infra**

Contém a comunicação com o banco, as entities do SQLAlchemy e os repositories responsáveis pela persistência.

**API**

Responsável pela comunicação HTTP, schemas Pydantic e exposição dos recursos da aplicação.

**Templates / Static**

Contém somente a camada de apresentação: páginas Jinja2, CSS e JavaScript do frontend.

## Fluxo da compra

O checkout segue, de forma simplificada, o fluxo:

```text
Cliente + Cartão
       ↓
     Carrinho
       ↓
  Calcular total
       ↓
Validar saldo
       ↓
Validar estoque
       ↓
Registrar histórico
       ↓
Atualizar estoque
       ↓
Atualizar saldo
       ↓
 Limpar carrinho
```

O histórico mantém o preço praticado no momento da compra, permitindo preservar a informação mesmo que o preço do produto seja alterado posteriormente.

## Modelo de dados

O PostgreSQL utilizado pelo projeto possui atualmente sete tabelas principais:

```text
cliente
├── cartao
├── carrinho
│   └── produto_carrinho
└── historico_compra
    └── item_historico

produto
├── produto_carrinho
└── item_historico
```

### Tabelas

- `cliente`: dados cadastrais dos clientes.
- `cartao`: cartões e saldos associados aos clientes.
- `produto`: catálogo, preços e estoque.
- `carrinho`: carrinho persistido do cliente.
- `produto_carrinho`: associação entre carrinho, produto e quantidade.
- `historico_compra`: registro de cada compra realizada.
- `item_historico`: itens comprados e preço praticado no momento da compra.

## Interface web

A interface utiliza o nome AUREA apenas como identidade visual da loja. Ela é servida pelo próprio FastAPI através de Jinja2.

A organização atual do frontend é:

```text
templates/
├── pages/
│   ├── base.html
│   ├── index.html
│   ├── loja.html
│   ├── conta.html
│   ├── sacola.html
│   ├── checkout.html
│   ├── historico.html
│   └── gestao.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        ├── api.js
        ├── common.js
        ├── home.js
        ├── loja.js
        ├── conta.js
        ├── sacola.js
        ├── checkout.js
        ├── historico.js
        └── gestao.js
```

A página de gestão permite administrar produtos pelo frontend, enquanto as demais páginas cuidam da navegação da loja e das etapas da compra.

## Requisitos

- Python 3.12+ recomendado
- PostgreSQL 18 (ou versão compatível com o projeto)
- Ambiente virtual Python

## Configuração

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

Depois:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente no `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Project_CPDI
DB_USER=postgres
DB_PASSWORD=sua_senha
```

> O arquivo `.env` deve permanecer fora do Git. Utilize o `.env.example` como referência quando disponível.

## Executando

A partir da raiz do projeto:

```bash
python -m uvicorn project.api.app:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000/
```

A documentação interativa da API:

```text
http://127.0.0.1:8000/docs
```

## Validação do projeto

O backend foi validado com operações reais no PostgreSQL através da API e consultas diretas ao banco.

Entre os fluxos já verificados estão:

- criação de cliente com carrinho persistido;
- cadastro e consulta de produtos;
- associação de cartão ao cliente;
- adição de produtos ao carrinho;
- adição repetida do mesmo produto com acumulação da quantidade;
- remoção de produto do carrinho;
- realização da compra;
- redução do saldo do cartão;
- redução do estoque;
- limpeza do carrinho;
- criação do histórico da compra;
- consulta do histórico através da API.

A documentação Swagger também foi utilizada para testar diretamente os endpoints REST.

## API

A API é organizada em rotas por recurso, incluindo operações para:

```text
clientes
produtos
cartões
carrinho
compras
histórico
```

Cada recurso possui seus schemas Pydantic e os repositories correspondentes na infraestrutura.

## Princípios adotados

O projeto procura aplicar Clean Architecture e DDD de maneira pragmática, sem transformar a aplicação em uma estrutura excessivamente complexa.

Entre os princípios utilizados:

- regras de negócio concentradas no domínio e nos casos de uso;
- domínio desacoplado de SQLAlchemy;
- persistência isolada em repositories;
- SQLAlchemy utilizado na camada de infraestrutura;
- FastAPI restrito à camada HTTP;
- schemas Pydantic utilizados para contratos de entrada e saída;
- frontend tratado como camada de apresentação;
- objetos de relacionamento, como `ProdutoCarrinho`, persistidos como parte do agregado de carrinho quando apropriado.

## Status

**Projeto funcional em desenvolvimento.**

A API e o fluxo principal de compra já estão funcionando e foram validados com persistência real. A interface web está integrada à API e continua sendo refinada como camada de apresentação.

## Autor

Projeto desenvolvido como trabalho final de formação em programação Python.
