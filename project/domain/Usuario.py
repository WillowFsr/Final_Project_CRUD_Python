from typing import Optional


class Usuario:
  def __init__(idade:int, nome: str, self, endereco:str, nacionalidade:str, id_usr: Optional[int] = None ):
    self.id_usr = id_usr
    self.idade = idade
    self.nome = nome
    self.endereco = endereco
    self.nacionalidade = nacionalidade

  # - > Methods
  

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
      raise ValueError(f"O nome do produto não pode ser vazio")
      
    self._nome = nome  

  @id_usr.setter
  def id_usr(self, id_usr: Optional[int]) -> None:
    if(id_prod is not None and not isinstance(id_prod,int)):
      raise TypeError("O ID do produto deverá ser um inteiro")
    self._id_usr = id_usr
  
  @endereco.setter
  def endereco(self, endereco:str) -> None:
    if (not isinstance(endereco,str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    if (not nome.strip()):
      raise ValueError(f"O endereco não pode ser vazio")
      
    self._endereco = endereco 

  @nacionalidade.setter
  def nacionalidade(self, nacionalidade:str) -> None:
    if (not isinstance(nacionalidade,str)):
      raise TypeError(f"A entrada deveria ser um texto(string)")
    if (not nome.strip()):
      raise ValueError(f"A nacionalidade não pode ser vazio")
      
    self._nacionalidade= nacionalidade
