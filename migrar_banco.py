#!/usr/bin/env python3
"""
Script para executar migrações do banco de dados
Adiciona a coluna valor_compra se não existir
"""

import os
from models import init_db, DATABASE_TYPE

def executar_migracao():
    """Executa a migração do banco de dados"""
    print("🔄 Executando migração do banco de dados...")
    print(f"📊 Tipo de banco: {DATABASE_TYPE}")
    
    try:
        init_db()
        print("✅ Migração executada com sucesso!")
        print("✅ Coluna 'valor_compra' adicionada (se não existia)")
        return True
    except Exception as e:
        print(f"❌ Erro ao executar migração: {e}")
        return False

if __name__ == '__main__':
    # Verificar se está usando PostgreSQL (Supabase)
    if DATABASE_TYPE == 'postgresql':
        print("🗄️  Conectando ao Supabase PostgreSQL...")
    else:
        print("🗄️  Usando SQLite local...")
    
    sucesso = executar_migracao()
    
    if sucesso:
        print("\n✅ Banco de dados atualizado!")
        print("💡 A coluna 'valor_compra' está disponível para uso.")
    else:
        print("\n❌ Falha na migração. Verifique as configurações do banco de dados.")
        exit(1)

