# tests/conftest.py
import sys
import os

print("Carregando conftest.py")
print(f"Diretório atual: {os.getcwd()}")
print(f"sys.path antes: {sys.path}")

# Adiciona o diretório `src` ao caminho de módulos do Python
sys.path.insert(0, '/home/vinicius/repos/premier_league_api/src')

print(f"sys.path depois: {sys.path}")
