from __future__ import annotations
import sys
import os

domain_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')
if domain_path not in sys.path:
    sys.path.append(domain_path)
from connection import iniciar_conexao

iniciar_conexao()