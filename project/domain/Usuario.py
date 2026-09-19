from __future__ import annotations
from typing import Optional, Any
from abc import ABC, abstractmethod

class Usuario(ABC):
  def __init__(self, nome: str, idade:int , endereco:str, nacionalidade:str):
    self.idade = idade
    self.nome = nome
    self.endereco = endereco
    self.nacionalidade = nacionalidade

  # - > Methods
  def to_dict(self) -> dict[str,Any]:
    return {
      "nome":self.nome,
      "idade":self.idade,
      "endereco":self.endereco,
      "nacionalidade":self.nacionalidade
    }

  def to_tuple(self) -> tuple[str, int, str, str]:
    return (self.nome, self.idade, self.endereco, self.nacionalidade)
  
  #this class is abstract, so it cannot implement from_db, only her childs
  @staticmethod
  @abstractmethod
  def from_db(linha: tuple) -> Usuario:
    pass
  
  def maior_de_idade(self) -> bool:
    return self.idade>=18
  
  #Getter
  @property
  def nome(self) -> str:
    return self._nome
  
  @property
  def idade(self) -> int:
    return self._idade
  
  @property
  def endereco(self) -> str:
    return self._endereco

  @property
  def nacionalidade(self) -> str:
    return self._nacionalidade
  
  #Setter
  @nome.setter
  def nome(self, nome:str) -> None:
    if (not isinstance(nome,str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    if (not nome.strip()):
      raise ValueError(f"O nome do Usuário não pode ser vazio")
      
    self._nome = nome  

  @endereco.setter
  def endereco(self, endereco:str) -> None:
    if (not isinstance(endereco,str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    if (not endereco.strip()):
      raise ValueError(f"O endereco não pode ser vazio")
      
    self._endereco = endereco 

  @nacionalidade.setter
  def nacionalidade(self, nacionalidade:str) -> None:
    if (not isinstance(nacionalidade,str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    if (not nacionalidade.strip()):
      raise ValueError(f"A nacionalidade não pode ser vazio")
      
    self._nacionalidade= nacionalidade

  @idade.setter
  def idade(self, idade: int) -> None:
    if(not isinstance(idade,int)):
      raise TypeError("A entrada deveria ser um número Inteiro")
    if(idade >140 or idade<0):
      raise ValueError("Entrada fora dos limites humanos")
    self._idade = idade