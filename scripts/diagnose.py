# diagnose.py
import os
from pathlib import Path

print("======================================================================")
print("  SCRIPT DE DIAGNÓSTICO DO ECOSSISTEMA SOFIA")
print("======================================================================")

# Define a raiz do projeto como o diretório onde este script está
project_root = Path(__file__).resolve().parent

print(f"\n[INFO] Raiz do Projeto Detectada: {project_root}\n")

print("[INFO] Verificando a estrutura de diretórios e arquivos __init__.py...")
print("----------------------------------------------------------------------")

# Lista de diretórios que DEVEM ser pacotes Python
required_packages = [
    project_root / "backend",
    project_root / "backend" / "app",
    project_root / "backend" / "app" / "routes",
]

all_ok = True

for package_path in required_packages:
    init_file = package_path / "__init__.py"
    
    # Verifica se o diretório existe
    if package_path.is_dir():
        # Verifica se o __init__.py existe dentro dele
        if init_file.is_file():
            print(f"[ ✅ SUCESSO ] Pacote encontrado: {package_path}")
        else:
            print(f"[ ❌ FALHA   ] O diretório existe, mas falta o __init__.py: {package_path}")
            all_ok = False
    else:
        print(f"[ ❌ FALHA   ] Diretório do pacote não encontrado: {package_path}")
        all_ok = False

print("----------------------------------------------------------------------")

if all_ok:
    print("\n[RESULTADO] A estrutura de pacotes do backend parece estar CORRETA.")
    print("O erro 'ModuleNotFoundError' provavelmente tem outra causa, possivelmente um erro de digitação em um nome de arquivo ou importação.")
else:
    print("\n[RESULTADO] A estrutura de pacotes está INCORRETA.")
    print("Crie os arquivos '__init__.py' que faltam nos diretórios marcados com 'FALHA' para resolver o problema.")

print("\n======================================================================")

