#!/bin/bash
# Script para iniciar o projeto localmente com Supabase

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando Controle de Estoque Localmente...${NC}\n"

# Verificar se env.local existe
if [ ! -f "env.local" ]; then
    echo -e "${YELLOW}⚠️  Arquivo env.local não encontrado!${NC}"
    echo "   Criando a partir do env.example..."
    cp env.example env.local
    echo -e "${YELLOW}   Por favor, edite o env.local com suas credenciais do Supabase${NC}"
    exit 1
fi

# Carregar variáveis de ambiente do env.local
echo -e "${BLUE}📋 Carregando variáveis de ambiente do env.local...${NC}"
export $(grep -v '^#' env.local | xargs)

# Verificar se as variáveis foram carregadas
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
    echo -e "${YELLOW}⚠️  Variáveis do Supabase não configuradas no env.local!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Variáveis de ambiente carregadas${NC}\n"

# Verificar se as dependências estão instaladas
echo -e "${BLUE}📦 Verificando dependências...${NC}"
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Flask não encontrado. Instalando dependências...${NC}"
    pip3 install -r requirements.txt
fi

if ! python3 -c "import psycopg2" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  psycopg2 não encontrado. Instalando...${NC}"
    pip3 install psycopg2-binary
fi

if ! python3 -c "import supabase" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  supabase não encontrado. Instalando...${NC}"
    pip3 install supabase
fi

echo -e "${GREEN}✅ Dependências OK${NC}\n"

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

