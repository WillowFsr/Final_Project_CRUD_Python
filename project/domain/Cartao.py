from __future__ import annotations
from typing import Optional, Any
from decimal import Decimal
from datetime import date

class Cartao:
  def __init__(self, numero: str, validade: date, cvv: str, bandeira: str, saldo: Decimal, id_cli: Optional[int] = None, id_cartao: Optional[int] = None ):
    self.id_cartao = id_cartao  
    self.id_cli = id_cli
    self.numero = numero
    self.validade = validade
    self.cvv = cvv
    self.bandeira = bandeira
    self.saldo = saldo

  # - > Methods
  def to_dict(self) -> dict[str, Any]:
    return {
      "id_cartao": self.id_cartao,
      "id_cli": self.id_cli,
      "numero": self.numero,
      "validade": self.validade,
      "cvv": self.cvv,
      "bandeira": self.bandeira,
      "saldo": self.saldo
    }
  
  def to_tuple(self) -> tuple[str, date, str, str, Decimal, Optional[int]]:
    return (self.numero, self.validade, self.cvv, self.bandeira, self.saldo, self.id_cli)
  
  @staticmethod
  def from_db(linha: tuple) -> Cartao:
    return Cartao(
      numero=linha[0],
      validade=linha[1],
      cvv=linha[2],
      bandeira=linha[3],
      saldo=linha[4],
      id_cli=linha[5],
      id_cartao=linha[6]
    )
  
  #Getters
  @property
  def id_cartao(self) -> Optional[int]:
    return self._id_cartao

  @property 
  def id_cli(self) -> Optional[int]:
    return self._id_cli

  @property     
  def numero(self) -> str:
    return self._numero

  @property
  def validade(self) -> date:
    return self._validade

  @property     
  def cvv(self) -> str:
    return self._cvv

  @property
  def bandeira(self) -> str:
    return self._bandeira

  @property 
  def saldo(self) -> Decimal:
    return self._saldo

  # #Setters
  @id_cartao.setter
  def id_cartao(self, id_cartao: Optional[int]) -> None:
    if (id_cartao is not None and not isinstance(id_cartao, int)):
      raise TypeError(f"A entrada deve ser um numero inteiro")
    self._id_cartao = id_cartao
  
  @id_cli.setter
  def id_cli(self, id_cli: Optional[int]) -> None:
    if(id_cli is not None and not isinstance(id_cli, int)):
      raise TypeError(f"A entrada deve ser um numero inteiro")
    self._id_cli = id_cli
  
  @numero.setter
  def numero(self, numero: str) -> None:
    if(not isinstance(numero, str)):
      raise TypeError(f"A entrada deve ser um texto (string)")
    if(not numero.strip()):
      raise ValueError(f"O número do cartão não pode ser vazio")
    self._numero = numero
  
  @validade.setter
  def validade(self, validade: date) -> None:
    if not isinstance(validade, date):
      raise TypeError("A validade deve ser do tipo date")
    self._validade = validade
  
  @cvv.setter
  def cvv(self, cvv: str) -> None:
    if(not isinstance(cvv, str)):
      raise TypeError(f"A entrada deve ser um texto(string)")
    if(not cvv.strip()):
      raise ValueError(f"O cvv do cartao nao pode ser nulo")
    self._cvv = cvv
  
  @bandeira.setter
  def bandeira(self, bandeira: str) -> None:
    if(not isinstance(bandeira, str)):
      raise TypeError(f"A entrada deve ser um texto(string)")
    if(not bandeira.strip()):
      raise ValueError(f"A bandeira do cartao nao pode ser nula")
    self._bandeira = bandeira
  
  @saldo.setter
  def saldo(self, saldo: Decimal) -> None:
    if(not isinstance(saldo, Decimal)):
      raise TypeError(f"Entrada incorreta, esperado um número")
    if(saldo < 0):
      raise ValueError(f"O dinheiro numa conta não pode ser menor que zero")
    self._saldo = saldo