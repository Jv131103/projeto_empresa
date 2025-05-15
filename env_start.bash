#!/bin/bash

# Função para ativar ou criar e ativar virtualenv automaticamente
auto_envon() {
    local ENV_DIR="`pwd`/env"  # Caminho do ambiente virtual na pasta atual

    # Se o env não existir, cria
    if [ ! -d "$ENV_DIR" ]; then
        echo -e "\e[33m🚧 Criando ambiente virtual em $ENV_DIR...\e[0m"
        python3 -m venv "$ENV_DIR"
    fi

    # Ativa o ambiente
    . "$ENV_DIR/bin/activate"

    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo -e "\e[32m🎉 Ambiente virtual ativado: $VIRTUAL_ENV\e[0m"
    else
        echo -e "\e[31m❌ Falha ao ativar ambiente virtual.\e[0m"
    fi
}

# Chama a função ao abrir o terminal

# Para chamar completo o código digite source env_start.bash
auto_envon
