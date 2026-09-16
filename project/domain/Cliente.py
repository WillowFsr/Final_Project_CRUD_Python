from typing import Optional
 
class Cliente:
  def __init__(self, nome_cliente: str, cpf_cliente: str, email_cliente: str, id_cliente: Optional[int] = None):
    self.id_cliente = id_cliente
    self.nome_cliente = nome_cliente
    self.cpf_cliente = cpf_cliente
    self.email_cliente = email_cliente
  
  


