from __future__ import annotations
import sys
import os

# Adiciona a pasta 'domain' ao caminho do Python para resolver os imports internos
domain_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'domain')
if domain_path not in sys.path:
    sys.path.append(domain_path)

from Cliente import Cliente
from Cartao import Cartao
from Carrinho import Carrinho
from Produto import Produto
from ProdutoCarrinho import ProdutoCarrinho
from ProcessadorPagamento import ProcessadorPagamento


def executar_testes_sistema() -> None:
    print("INICIALIZANDO TESTES DE ROBUSTEZ DO SISTEMA")

    produto_1 = Produto(
        nome="Notebook Gamer",
        preco=5000.0,
        descricao="Notebook de alto desempenho",
        estoque=5,
        id_prod=1
    )
    
    produto_2 = Produto(
        nome="Mouse Sem Fio",
        preco=150.0,
        descricao="Mouse ergonomico otico",
        estoque=10,
        id_prod=2
    )

    cliente = Cliente(
        nome="Carlos Silva",
        idade=30,
        endereco="Rua Exemplo, 123",
        nacionalidade="Brasileira",
        id_cli=1
    )

    cartao = Cartao(
        numero=101,
        validade="12/30",
        cvv="123",
        bandeira="Visa",
        valor=10000.0,
        id_cartao=1
    )
    cliente.inserir_cartao(cartao)

    print("\n[TESTE 1] Adicao de produtos ao carrinho e calculo de total")
    cliente.carrinho.adicionar_produto(produto_1, 1)
    cliente.carrinho.adicionar_produto(produto_2, 2)
    
    total_esperado = (5000.0 * 1) + (150.0 * 2)
    total_calculado = cliente.carrinho.calcular_total()
    
    assert total_calculado == total_esperado, f"Erro no calculo do total: {total_calculado}"
    print(f"Total do carrinho validado com sucesso: R$ {total_calculado}")

    print("\n[TESTE 2] Processamento de pagamento bem-sucedido")
    estoque_inicial_p1 = produto_1.estoque
    estoque_inicial_p2 = produto_2.estoque
    saldo_inicial_cartao = cartao.valor

    ProcessadorPagamento.processarcompra(cliente, id_cartao=101)

    assert produto_1.estoque == estoque_inicial_p1 - 1
    assert produto_2.estoque == estoque_inicial_p2 - 2
    assert cartao.valor == saldo_inicial_cartao - total_esperado
    assert len(cliente.carrinho._produto_carrinho) == 0
    print("Pagamento processado com sucesso, estoque atualizado e carrinho limpo.")

    print("\n[TESTE 3] Tentativa de compra com carrinho vazio")
    try:
        ProcessadorPagamento.processarcompra(cliente, id_cartao=101)
        raise AssertionError("Deveria ter barrado carrinho vazio")
    except ValueError as e:
        print(f"Excecao capturada corretamente: {e}")

    print("\n[TESTE 4] Tentativa de compra com saldo insuficiente")
    cliente.carrinho.adicionar_produto(produto_1, 3)
    cartao.valor = 100.0
    try:
        ProcessadorPagamento.processarcompra(cliente, id_cartao=101)
        raise AssertionError("Deveria ter barrado saldo insuficiente")
    except ValueError as e:
        print(f"Excecao capturada corretamente: {e}")

    print("\n[TESTE 5] Tentativa de compra com estoque excedido")
    cartao.valor = 50000.0
    produto_1.estoque = 1
    cliente.carrinho.limpar_carrinho()
    
    try:
        cliente.carrinho.adicionar_produto(produto_1, 5)
        ProcessadorPagamento.processarcompra(cliente, id_cartao=101)
        raise AssertionError("Deveria ter barrado estoque insuficiente")
    except ValueError as e:
        print(f"Excecao capturada corretamente: {e}")

    print("\nTODOS OS TESTES EXECUTADOS COM SUCESSO")


if __name__ == "__main__":
    executar_testes_sistema()