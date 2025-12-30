#!/usr/bin/env python3
"""
Script para verificar conexão e dados no banco PostgreSQL do Railway
"""
import os
import sys

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from models import get_db, produto_para_dict, DATABASE_TYPE
    from psycopg2.extras import RealDictCursor
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("💡 Certifique-se de que todas as dependências estão instaladas")
    sys.exit(1)

def verificar_banco():
    """Verifica conexão e dados do banco"""
    print("=" * 60)
    print("🔍 Verificando Banco de Dados")
    print("=" * 60)
    
    # Verificar tipo de banco
    print(f"\n📊 Tipo de banco: {DATABASE_TYPE.upper()}")
    
    if DATABASE_TYPE != 'postgresql':
        print("⚠️  Este script é para PostgreSQL. Configure DATABASE_TYPE=postgresql")
        return
    
    try:
        # Tentar conectar
        print("\n🔌 Tentando conectar ao banco...")
        conn = get_db()
        print("✅ Conexão estabelecida com sucesso!")
        
        # Verificar tabela
        if DATABASE_TYPE == 'postgresql':
            cursor = conn.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'produtos'
        """)
        tabela_existe = cursor.fetchone()
        
        if not tabela_existe:
            print("\n⚠️  Tabela 'produtos' não encontrada!")
            print("💡 Execute a inicialização do banco primeiro")
            conn.close()
            return
        
        print("✅ Tabela 'produtos' encontrada!")
        
        # Verificar estrutura da tabela
        print("\n📋 Estrutura da tabela:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'produtos'
            ORDER BY ordinal_position
        """)
        colunas = cursor.fetchall()
        for coluna in colunas:
            print(f"   - {coluna[0]}: {coluna[1]} ({'NULL' if coluna[2] == 'YES' else 'NOT NULL'})")
        
        # Contar produtos
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total_produtos = cursor.fetchone()[0]
        print(f"\n📦 Total de produtos: {total_produtos}")
        
        if total_produtos > 0:
        # Listar alguns produtos
        print("\n📋 Primeiros 5 produtos:")
        if DATABASE_TYPE == 'postgresql':
            cursor.execute("""
                SELECT * FROM produtos 
                ORDER BY data_atualizacao DESC 
                LIMIT 5
            """)
            produtos = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT * FROM produtos 
                ORDER BY data_atualizacao DESC 
                LIMIT 5
            """)
            produtos = cursor.fetchall()
        
        for produto in produtos:
            produto_dict = produto_para_dict(produto)
                print(f"\n   ID: {produto_dict['id']}")
                print(f"   Título: {produto_dict['titulo']}")
                print(f"   ML: {produto_dict['quantidade_mercado_livre']}")
                print(f"   Shopee: {produto_dict['quantidade_shopee']}")
                print(f"   Total: {produto_dict['quantidade']}")
                print(f"   Tipo ML: {type(produto_dict['quantidade_mercado_livre'])}")
                print(f"   Tipo Shopee: {type(produto_dict['quantidade_shopee'])}")
                print(f"   Tipo Total: {type(produto_dict['quantidade'])}")
        else:
            print("\nℹ️  Nenhum produto cadastrado ainda")
        
        # Verificar dados problemáticos
        print("\n🔍 Verificando dados problemáticos...")
        cursor.execute("""
            SELECT id, titulo, quantidade_mercado_livre, quantidade_shopee
            FROM produtos
            WHERE quantidade_mercado_livre IS NULL 
               OR quantidade_shopee IS NULL
               OR quantidade_mercado_livre::text ~ '[^0-9]'
               OR quantidade_shopee::text ~ '[^0-9]'
        """)
        problemas = cursor.fetchall()
        
        if problemas:
            print(f"⚠️  Encontrados {len(problemas)} produtos com dados problemáticos:")
            for problema in problemas:
                print(f"   - ID {problema[0]}: {problema[1]}")
                print(f"     ML: {problema[2]} (tipo: {type(problema[2])})")
                print(f"     Shopee: {problema[3]} (tipo: {type(problema[3])})")
        else:
            print("✅ Nenhum problema encontrado nos dados!")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Verificação concluída!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro ao verificar banco: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(verificar_banco())

