#!/usr/bin/env python3
"""
Script de setup para IA do Lumber Inc.
"""

import subprocess
import sys
import os

def check_adb_installation():
    """Verifica se ADB está instalado"""
    try:
        result = subprocess.run(["adb", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ ADB encontrado")
            return True
        else:
            print("✗ ADB não encontrado")
            return False
    except FileNotFoundError:
        print("✗ ADB não encontrado no PATH")
        return False

def install_requirements():
    """Instala dependências Python"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow", "opencv-python", "numpy"], 
                      check=True)
        print("✓ Dependências Python instaladas")
        return True
    except subprocess.CalledProcessError:
        print("✗ Erro ao instalar dependências Python")
        return False

def create_directories():
    """Cria diretórios necessários"""
    directories = ['templates', 'screenshots', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Diretório '{directory}' criado/verificado")

def main():
    print("=== Setup da IA do Lumber Inc. ===")
    
    # Verificar ADB
    if not check_adb_installation():
        print("\nPor favor, instale o ADB:")
        print("sudo apt update && sudo apt install -y android-sdk-platform-tools")
        return
    
    # Criar diretórios
    create_directories()
    
    # Instalar dependências
    if not install_requirements():
        print("\nErro na instalação das dependências")
        return
    
    print("\n✓ Setup concluído com sucesso!")
    print("\nPróximos passos:")
    print("1. Conecte seu dispositivo Android via USB")
    print("2. Ative a depuração USB no dispositivo")
    print("3. Execute: python lumber_ai.py")
    print("\nPara calibrar coordenadas, execute: python calibrate.py")

if __name__ == "__main__":
    main()