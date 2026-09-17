from __future__ import annotations
from typing import Optional, Any
from abc import ABC, abstractmethod

class Usuario(ABC):
  def __init__(self,idade:int, nome: str, endereco:str, nacionalidade:str, id_usr: Optional[int] = None ):
    self.id_usr = id_usr
    self.idade = idade
    self.nome = nome
    self.endereco = endereco
    self.nacionalidade = nacionalidade

  # - > Methods
  def to_dict(self) -> dict[str,Any]:
    return {
      "id_usr":self.id_usr,
      "nome":self.nome,
      "idade":self.idade,
      "endereco":self.endereco,
      "nacionalidade":self.nacionalidade
    }

  def to_tuple(self) -> tuple[str, int, str, str]:
    return (self.nome,self.idade,self.endereco, self.nacionalidade)
  
  #this class is abstract, so it cannot implement from_db, only her childs
  @abstractmethod
  @staticmethod
  def from_db(linha: tuple) ->  Usuario:
    pass
  
  def maior_de_idade(self) -> bool:
    return self.idade>=18
  
  def atualizar_endereco(self, novo_endereco: str) -> None:
        self.endereco = novo_endereco
  
  #Getter
  @property
  def nome(self) -> str:
    return self._nome

  @property
  def id_usr(self) -> Optional[int]:
    return self._id_usr
  
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

  @id_usr.setter
  def id_usr(self, id_usr: Optional[int]) -> None:
    if(id_usr is not None and not isinstance(id_usr,int)):
      raise TypeError("O ID do usuário deverá ser um inteiro")
    self._id_usr = id_usr
  
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