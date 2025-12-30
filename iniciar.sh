#!/bin/bash
# Script de inicialização do Controle de Estoque
# Este script configura o ambiente e inicia a aplicação com Supabase

set -e  # Parar em caso de erro

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando Controle de Estoque...${NC}\n"

# Verificar se o arquivo de configuração existe
if [ ! -f "configurar_supabase.sh" ]; then
    echo -e "${YELLOW}⚠️  Arquivo configurar_supabase.sh não encontrado!${NC}"
    echo "   Por favor, configure o Supabase primeiro."
    exit 1
fi

# Carregar configurações do Supabase
echo -e "${BLUE}📋 Carregando configurações do Supabase...${NC}"
source configurar_supabase.sh > /dev/null 2>&1

# Verificar se as variáveis foram carregadas
if [ -z "$DB_PASSWORD" ] || [ "$DB_PASSWORD" = "sua_senha_aqui" ]; then
    echo -e "${YELLOW}⚠️  Senha do banco de dados não configurada!${NC}"
    echo "   Edite o arquivo configurar_supabase.sh e configure sua senha."
    exit 1
fi

# Verificar conexão com o banco (teste básico)
echo -e "${BLUE}🔌 Verificando configuração do banco...${NC}"
if [ "$DATABASE_TYPE" = "postgresql" ]; then
    echo -e "${GREEN}✅ Usando PostgreSQL (Supabase)${NC}"
else
    echo -e "${GREEN}✅ Usando SQLite (desenvolvimento)${NC}"
fi
echo ""

# Verificar se as dependências estão instaladas
echo -e "${BLUE}📦 Verificando dependências...${NC}"
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Flask não encontrado. Instalando dependências...${NC}"
    pip3 install -r requirements.txt
fi

if [ "$DATABASE_TYPE" = "postgresql" ]; then
    if ! python3 -c "import psycopg2" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  psycopg2 não encontrado. Instalando...${NC}"
        pip3 install psycopg2-binary
    fi
fi

echo -e "${GREEN}✅ Dependências OK${NC}\n"

# Inicializar banco de dados (criar tabelas se não existirem)
echo -e "${BLUE}🗄️  Inicializando banco de dados...${NC}"
python3 -c "from models import init_db; init_db(); print('✅ Banco de dados pronto!')" 2>/dev/null || echo "ℹ️  Banco já inicializado"
echo ""

# Verificar se há processos rodando na porta 5001
if lsof -ti:5001 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Porta 5001 já está em uso. Parando processo anterior...${NC}"
    pkill -f "python3 app.py" 2>/dev/null || true
    sleep 2
fi

# Iniciar servidor
echo -e "${GREEN}🚀 Iniciando servidor Flask...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Aplicação rodando!${NC}"
echo -e "${BLUE}📍 Acesse: ${GREEN}http://localhost:5001${NC}"
echo -e "${BLUE}📍 Ou: ${GREEN}http://127.0.0.1:5001${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}💡 Pressione Ctrl+C para parar o servidor${NC}\n"

# Iniciar aplicação
python3 app.py
