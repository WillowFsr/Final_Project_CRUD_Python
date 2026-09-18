from __future__ import annotations
from typing import Optional,Any

class Cartao:
  def __init__(self, numero: int, validade: str, cvv: str, bandeira: str, valor:float,id_usr: Optional[int] = None, id_cartao:Optional[int] = None ):
    self.id_cartao = id_cartao
    self.id_usr = id_usr
    self.numero = numero
    self.validade = validade
    self.cvv = cvv
    self.bandeira = bandeira
    self.valor = valor

  # - > Methods
  def to_dict(self) -> dict[str, Any]:
    return {
      "id_cartao": self.id_cartao,
      "id_usr": self.id_usr,
      "numero": self.numero,
      "validade": self.validade,
      "cvv":self.cvv,
      "bandeira": self.bandeira,
      "valor": self.valor

    }
  
  def to_tuple(self) -> tuple[int, str, str, str, float,Optional[int]]:
    return (self.numero, self.validade, self.cvv, self.bandeira, self.valor, self.id_usr)
  
  @staticmethod
  def from_db(lista:tuple) -> Cartao:
    return Cartao(
      numero= lista[0],
      validade=lista[1],
      cvv=lista[2],
      bandeira=lista[3],
      valor=lista[4],
      id_usr=lista[5],
      id_cartao=lista[6]
    )
  
  #Getters
  @property
  def id_cartao(self) -> Optional[int]:
    return self._id_cartao

  @property 
  def id_usr(self) -> Optional[int]:
    return self._id_usr

  @property    
  def numero(self) -> int:
    return self._numero

  @property
  def validade(self) -> str:
    return self._validade

  @property    
  def cvv(self) -> str:
    return self._cvv

  @property
  def bandeira(self) -> str:
    return self._bandeira

  @property 
  def valor(self) -> float:
    return self._valor

  # #Setters
  @id_cartao.setter
  def id_cartao(self, id_cartao:Optional[int]) -> None:
    if (id_cartao is not None and not isinstance(id_cartao, int)):
      raise TypeError(f"A entrada deve ser um numero inteiro")
    self._id_cartao = id_cartao
  
  @id_usr.setter
  def id_usr(self, id_usr:Optional[int]) -> None:
    if(id_usr is not None and not isinstance(id_usr,int)):
      raise TypeError(f"A entrada deve ser um numero inteiro")
    self._id_usr = id_usr
  
  @numero.setter
  def numero(self, numero:int) -> None:
    if(not isinstance(numero,int)):
      raise TypeError(f"A entrada deve ser um numero inteiro")
    if(numero <0):
      raise ValueError(f"A entrada nao pode ser menor ou igual que zero")
    self._numero = numero
  
  @validade.setter
  def validade(self, validade:str) -> None:
    if(not isinstance(validade, str)):
      raise TypeError(f"A entrada deve ser um texto (string)")
    if(not validade.strip()):
      raise ValueError(f"A validade do cartao nao pode ser vazia")
    self._validade = validade
  
  @cvv.setter
  def cvv(self, cvv:str) -> None:
    if(not isinstance(cvv,str)):
      raise TypeError(f"A entrada deve ser um texto(string)")
    if(not cvv.strip()):
      raise ValueError(f"O cvv do cartao nao pode ser nulo")
    self._cvv = cvv
  
  @bandeira.setter
  def bandeira(self, bandeira:str) -> None:
    if(not isinstance(bandeira,str)):
      raise TypeError(f"A entrada deve ser um texto(string)")
    if(not bandeira.strip()):
      raise ValueError(f"A bandeira do cartao nao pode ser nula")
    self._bandeira = bandeira
  
  @valor.setter
  def valor(self, valor:float|int) -> None:
    if(not isinstance(valor, (float,int))):
      raise TypeError(f"Entrada incorreta, esperado um número")
    if(valor <0):
      raise ValueError(f"O dinheiro numa conta não pode ser menor que zero")
    self._valor = float(valor)