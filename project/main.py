import sys
import os

# Adiciona o diretório "Projeto Final" (pai de 'project') ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora o Python sabe de onde tirar o 'project'
from project.infra.repository.Cliente_Repository import Cliente_Repository
from project.infra.repository.Produto_Repository import Produto_Repository
from project.domain.Cliente import Cliente
from project.domain.Produto import Produto

def testar_repositorios():
    print("Iniciando testes da infraestrutura e banco de dados...")

    cliente_repo = Cliente_Repository()
    produto_repo = Produto_Repository()

    print("\n--- Testando Inserções (Insert) ---")
    
    # IMPORTANTE: Ajuste os campos abaixo caso o seu construtor em domain seja um pouco diferente
    novo_cliente = Cliente(nome="William Saraiva", email="william@exemplo.com")
    cliente_repo.insert(novo_cliente)
    print("Cliente enviado para o banco com sucesso!")

    novo_produto = Produto(nome="Notebook", preco=3500.50, quantidade_estoque=10)
    produto_repo.insert(novo_produto)
    print("Produto enviado para o banco com sucesso!")

    print("\n--- Testando Consultas (Search por ID) ---")
    
    cliente_banco = cliente_repo.search(1)
    if cliente_banco:
        print(f"Cliente retornado do Postgres: {cliente_banco.nome}")
    else:
        print("Cliente ID 1 não encontrado.")
        
    produto_banco = produto_repo.search(1)
    if produto_banco:
        print(f"Produto retornado do Postgres: {produto_banco.nome}")
    else:
        print("Produto ID 1 não encontrado.")

if __name__ == "__main__":
    testar_repositorios()