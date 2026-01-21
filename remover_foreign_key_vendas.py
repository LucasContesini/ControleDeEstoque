#!/usr/bin/env python3
"""
Script para remover completamente a foreign key de vendas
Isso garante que as vendas nunca sejam deletadas quando um produto for deletado
"""

import os
from models import DATABASE_TYPE, get_db
from db_helper import get_cursor

def remover_foreign_key():
    """Remove a foreign key de vendas para preservar vendas mesmo se produto for deletado"""
    print("🔄 Removendo foreign key de vendas...")
    print(f"📊 Tipo de banco: {DATABASE_TYPE}")
    
    try:
        conn = get_db()
        cursor = get_cursor(conn)
        
        if DATABASE_TYPE == 'postgresql':
            # Encontrar todas as foreign keys na tabela vendas
            cursor.execute("""
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE table_name = 'vendas'
                AND constraint_type = 'FOREIGN KEY'
            """)
            constraints = cursor.fetchall()
            
            if constraints:
                for constraint in constraints:
                    constraint_name = constraint[0] if isinstance(constraint, tuple) else constraint.get('constraint_name', '')
                    if constraint_name:
                        try:
                            cursor.execute(f'ALTER TABLE vendas DROP CONSTRAINT {constraint_name}')
                            print(f"✅ Foreign key {constraint_name} removida")
                        except Exception as e:
                            print(f"⚠️  Erro ao remover {constraint_name}: {e}")
            else:
                print("ℹ️  Nenhuma foreign key encontrada (já removida ou nunca existiu)")
            
            conn.commit()
        else:
            # SQLite - recriar tabela sem foreign key
            print("ℹ️  SQLite: recriando tabela sem foreign key...")
            
            # Verificar se há dados
            cursor.execute('SELECT COUNT(*) as total FROM vendas')
            total = cursor.fetchone()
            total_vendas = total[0] if isinstance(total, tuple) else total.get('total', 0) if isinstance(total, dict) else 0
            
            if total_vendas > 0:
                print(f"⚠️  Há {total_vendas} vendas. Fazendo backup...")
                # Fazer backup dos dados
                cursor.execute('SELECT * FROM vendas')
                vendas_backup = cursor.fetchall()
                
                # Criar tabela temporária
                cursor.execute('''
                    CREATE TABLE vendas_temp AS SELECT * FROM vendas
                ''')
                
                # Dropar tabela antiga
                cursor.execute('DROP TABLE vendas')
                
                # Criar nova tabela SEM foreign key
                cursor.execute('''
                    CREATE TABLE vendas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        produto_id INTEGER,
                        produto_titulo TEXT,
                        valor_venda REAL NOT NULL,
                        valor_compra REAL NOT NULL,
                        data_venda TEXT NOT NULL,
                        onde_vendeu TEXT NOT NULL CHECK (onde_vendeu IN ('mercado_livre', 'shopee')),
                        observacoes TEXT,
                        data_criacao TEXT NOT NULL
                    )
                ''')
                
                # Restaurar dados
                for venda in vendas_backup:
                    if isinstance(venda, dict):
                        cursor.execute('''
                            INSERT INTO vendas (id, produto_id, produto_titulo, valor_venda, valor_compra, 
                                               data_venda, onde_vendeu, observacoes, data_criacao)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            venda.get('id'),
                            venda.get('produto_id'),
                            venda.get('produto_titulo'),
                            venda.get('valor_venda'),
                            venda.get('valor_compra'),
                            venda.get('data_venda'),
                            venda.get('onde_vendeu'),
                            venda.get('observacoes'),
                            venda.get('data_criacao')
                        ))
                    else:
                        # Tuple - assumir ordem padrão
                        cursor.execute('''
                            INSERT INTO vendas (id, produto_id, produto_titulo, valor_venda, valor_compra, 
                                               data_venda, onde_vendeu, observacoes, data_criacao)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', venda)
                
                # Remover tabela temporária
                cursor.execute('DROP TABLE vendas_temp')
                print("✅ Tabela recriada sem foreign key")
            else:
                # Sem dados, apenas recriar
                cursor.execute('DROP TABLE IF EXISTS vendas')
                cursor.execute('''
                    CREATE TABLE vendas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        produto_id INTEGER,
                        produto_titulo TEXT,
                        valor_venda REAL NOT NULL,
                        valor_compra REAL NOT NULL,
                        data_venda TEXT NOT NULL,
                        onde_vendeu TEXT NOT NULL CHECK (onde_vendeu IN ('mercado_livre', 'shopee')),
                        observacoes TEXT,
                        data_criacao TEXT NOT NULL
                    )
                ''')
                print("✅ Tabela recriada sem foreign key")
            
            conn.commit()
        
        cursor.close()
        conn.close()
        
        print("✅ Foreign key removida com sucesso!")
        print("💡 Agora as vendas NUNCA serão deletadas quando um produto for deletado")
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Erro ao executar migração: {e}")
        return False

if __name__ == '__main__':
    sucesso = remover_foreign_key()
    
    if sucesso:
        print("\n✅ Migração concluída!")
        print("💡 As vendas agora são completamente independentes dos produtos")
    else:
        print("\n❌ Falha na migração. Verifique as configurações do banco de dados.")
        exit(1)

