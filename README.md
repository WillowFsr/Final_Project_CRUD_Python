# Guia do Projeto e Fundamentos de Persistência

Documento técnico de referência cobrindo a estrutura atual do projeto, princípios de Clean Architecture/DDD, princípios SOLID e validação de dados.

---

## 1. Estrutura e Camadas do Projeto

A aplicação adota uma separação clara de responsabilidades no diretório `project/`, garantindo o isolamento das regras de negócio em relação aos detalhes de infraestrutura:

```text
Final_Project_CRUD_Python/
└── project/
    ├── database/         # Configuração de conexão e comunicação direta com PostgreSQL (Psycopg 3)
    ├── domain/           # Entidades e regras de negócio puras (Produto, Cliente, Carrinho, etc.)
    ├── repository/       # Ponte de persistência (mapeia banco de dados <-> entidades do domínio)
    ├── .env.exemple      # Modelo de variáveis de ambiente
    ├── main.py           # Ponto de entrada e orquestração do sistema
    └── requirements.txt  # requisitos para facilitar a instalação de dependências
```
---