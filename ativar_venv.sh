#!/bin/bash

# Nome do diretório do ambiente virtual
VENV_DIR="venv"

# Verifica se o diretório do venv já existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Criando o ambiente virtual..."
    python3 -m venv "$VENV_DIR"
fi

# Ativa o ambiente virtual
echo "Ativando o ambiente virtual..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
# Verifica se requirements.txt existe e instala as dependências
if [ -f "requirements.txt" ]; then
    echo "Instalando as dependências Python..."
    pip install -r requirements.txt
else
    echo "Arquivo requirements.txt não encontrado."
fi

# Instala o SAGA GIS usando apt-get
echo "Instalando SAGA GIS..."
# sudo apt-get update
sudo apt-get install -y saga  # python3

echo "Ambiente virtual configurado e dependências instaladas."
