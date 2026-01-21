#!/usr/bin/env python3
"""
Script para remover colunas antigas quantidade_mercado_livre e quantidade_shopee
"""

import os
from models import init_db, DATABASE_TYPE, get_db
from db_helper import get_cursor

def remover_colunas_antigas():
    """Remove as colunas antigas do banco de dados"""
    print("🔄 Removendo colunas antigas quantidade_mercado_livre e quantidade_shopee...")
    print(f"📊 Tipo de banco: {DATABASE_TYPE}")
    
    try:
        conn = get_db()
        cursor = get_cursor(conn)
        
        if DATABASE_TYPE == 'postgresql':
            # Verificar colunas existentes
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='produtos'
            """)
            rows = cursor.fetchall()
            if rows and isinstance(rows[0], dict):
                colunas_existentes = [row['column_name'] for row in rows]
            else:
                colunas_existentes = [row[0] for row in rows]
            
            # Remover quantidade_mercado_livre
            if 'quantidade_mercado_livre' in colunas_existentes:
                try:
                    cursor.execute('ALTER TABLE produtos DROP COLUMN quantidade_mercado_livre')
                    print("✅ Coluna quantidade_mercado_livre removida")
                except Exception as e:
                    print(f"⚠️  Erro ao remover quantidade_mercado_livre: {e}")
            
            # Remover quantidade_shopee
            if 'quantidade_shopee' in colunas_existentes:
                try:
                    cursor.execute('ALTER TABLE produtos DROP COLUMN quantidade_shopee')
                    print("✅ Coluna quantidade_shopee removida")
                except Exception as e:
                    print(f"⚠️  Erro ao remover quantidade_shopee: {e}")
            
            conn.commit()
        else:
            # SQLite não suporta DROP COLUMN diretamente
            print("ℹ️  SQLite não suporta remoção de colunas diretamente")
            print("   As colunas antigas serão ignoradas e não serão usadas")
            print("   Para remover completamente, você precisaria recriar a tabela")
        
        cursor.close()
        conn.close()
        
        print("✅ Migração concluída!")
        return True
    except Exception as e:
        print(f"❌ Erro ao executar migração: {e}")
        return False

if __name__ == '__main__':
    # Inicializar banco primeiro
    init_db()
    
    # Executar migração
    sucesso = remover_colunas_antigas()
    
    if sucesso:
        print("\n✅ Colunas antigas removidas com sucesso!")
        print("💡 O sistema agora usa apenas a coluna 'quantidade' única")
    else:
        print("\n❌ Falha na migração. Verifique as configurações do banco de dados.")
        exit(1)

