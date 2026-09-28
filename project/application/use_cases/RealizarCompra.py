from __future__ import annotations
from decimal import Decimal
#domain importations
from project.domain.Carrinho import Carrinho as Carrinho_Domain
from project.domain.Produto import Produto as Produto_Domain

#repository importations
from project.infra.repository.Cliente_Repository import Cliente_Repository as Cliente_Repo
from project.infra.repository.Produto_Repository import Produto_Repository as Produto_Repo
from project.infra.repository.Cartao_Repository import Cartao_Repository as Cartao_Repo
from project.infra.repository.Carrinho_Repository import Carrinho_Repository as Carrinho_Repo

class RealizarCompra:
  
  @staticmethod
  def verificar_estoque(produto:Produto_Domain,quantidade_compra:int) -> bool:
    return produto.estoque >= quantidade_compra

  
  def realizar_compra(self, id_cliente:int, id_cartao:int) -> bool:
    if (not isinstance(id_cartao, int) or not isinstance(id_cliente, int)):
      return False
    if (id_cartao<1 or id_cliente<1):
      return False
    
    cartao_repo = Cartao_Repo()
    cliente_repo = Cliente_Repo()
    produto_repo = Produto_Repo()
    carrinho_repo = Carrinho_Repo()
    cliente = cliente_repo.search(id_cliente)
    
    if (not cliente):
      return False
    
    carrinho = cliente.carrinho
    
    if (not carrinho):
      return False
    
    itens = carrinho.produto_no_carrinho()
    
    if (not itens):
      return False
    
    cartao = None
    
    for cartao_cliente in cliente.cartoes:
      if cartao_cliente.id_cartao == id_cartao:
        cartao = cartao_cliente
        break
      
    if (not cartao):
      return False
    
    valor_total = carrinho.calcular_total()
    if cartao.saldo < valor_total:
      return False
    
    for item in itens:
      if not self.verificar_estoque(item.produto,item.quantidade):
        return False
    
    from project.infra.repository.Historico_Repository import Historico_Compra_Repository as Historico
    
    historico = Historico.registrar_compra(id_cliente,valor_total,itens)
    
    if (not historico):
      return False
    
    for item in itens:
      item.produto.estoque -= item.quantidade
      
    for item in itens:
      if ( not produto_repo.update(item.produto.id_prod,item.produto)):
        return False
      
    cartao.saldo -= valor_total
    if (not cartao_repo.update(id_cartao,cartao)):
      return False
    
    carrinho.limpar_carrinho()
    if (not carrinho_repo.update(carrinho)):
      return False
    return True
      
