#!/usr/bin/env python3
"""
Script para alterar a foreign key de vendas de ON DELETE CASCADE para ON DELETE SET NULL
"""

import os
from models import DATABASE_TYPE, get_db
from db_helper import get_cursor

def alterar_foreign_key():
    """Altera a foreign key para preservar vendas quando produto é deletado"""
    print("🔄 Alterando foreign key de vendas...")
    print(f"📊 Tipo de banco: {DATABASE_TYPE}")
    
    try:
        conn = get_db()
        cursor = get_cursor(conn)
        
        if DATABASE_TYPE == 'postgresql':
            # Verificar constraint atual
            cursor.execute("""
                SELECT rc.constraint_name, rc.delete_rule
                FROM information_schema.referential_constraints rc
                JOIN information_schema.table_constraints tc ON rc.constraint_name = tc.constraint_name
                WHERE tc.table_name = 'vendas'
                AND tc.constraint_type = 'FOREIGN KEY'
            """)
            fk_info = cursor.fetchone()
            
            if fk_info:
                if isinstance(fk_info, dict):
                    constraint_name = fk_info.get('constraint_name', '')
                    delete_rule = fk_info.get('delete_rule', '')
                else:
                    constraint_name = fk_info[0] if len(fk_info) > 0 else ''
                    delete_rule = fk_info[1] if len(fk_info) > 1 else ''
                
                print(f"📌 Constraint encontrada: {constraint_name} (delete_rule: {delete_rule})")
                
                if delete_rule == 'CASCADE':
                    # Dropar a constraint antiga
                    try:
                        cursor.execute(f'ALTER TABLE vendas DROP CONSTRAINT {constraint_name}')
                        print(f"✅ Constraint {constraint_name} removida")
                    except Exception as e:
                        print(f"⚠️  Erro ao remover constraint: {e}")
                        # Tentar com nome padrão
                        try:
                            cursor.execute('ALTER TABLE vendas DROP CONSTRAINT vendas_produto_id_fkey')
                            print("✅ Constraint removida (nome padrão)")
                        except:
                            pass
                    
                    # Criar nova constraint com ON DELETE SET NULL
                    try:
                        cursor.execute('''
                            ALTER TABLE vendas
                            ADD CONSTRAINT vendas_produto_id_fkey
                            FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE SET NULL
                        ''')
                        print("✅ Nova constraint criada com ON DELETE SET NULL")
                    except Exception as e:
                        print(f"⚠️  Erro ao criar constraint: {e}")
                elif delete_rule == 'SET NULL':
                    print("✅ Constraint já está configurada corretamente (SET NULL)")
                else:
                    print(f"⚠️  Delete rule desconhecido: {delete_rule}")
            else:
                # Não há constraint, criar uma
                print("📌 Nenhuma constraint encontrada, criando nova...")
                try:
                    cursor.execute('''
                        ALTER TABLE vendas
                        ADD CONSTRAINT vendas_produto_id_fkey
                        FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE SET NULL
                    ''')
                    print("✅ Constraint criada com ON DELETE SET NULL")
                except Exception as e:
                    print(f"⚠️  Erro ao criar constraint: {e}")
            
            conn.commit()
        else:
            # SQLite - recriar tabela com nova constraint
            print("ℹ️  SQLite: recriando tabela com nova constraint...")
            
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
                
                # Criar nova tabela com constraint correta
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
                        data_criacao TEXT NOT NULL,
                        FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE SET NULL
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
                        # Tuple
                        cursor.execute('''
                            INSERT INTO vendas (id, produto_id, produto_titulo, valor_venda, valor_compra, 
                                               data_venda, onde_vendeu, observacoes, data_criacao)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', venda)
                
                # Remover tabela temporária
                cursor.execute('DROP TABLE vendas_temp')
                print("✅ Tabela recriada com constraint correta")
            else:
                # Sem dados, apenas recriar
                cursor.execute('DROP TABLE vendas')
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
                        data_criacao TEXT NOT NULL,
                        FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE SET NULL
                    )
                ''')
                print("✅ Tabela recriada com constraint correta")
            
            conn.commit()
        
        cursor.close()
        conn.close()
        
        print("✅ Migração concluída!")
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Erro ao executar migração: {e}")
        return False

if __name__ == '__main__':
    sucesso = alterar_foreign_key()
    
    if sucesso:
        print("\n✅ Foreign key alterada com sucesso!")
        print("💡 Agora as vendas serão preservadas quando um produto for deletado")
    else:
        print("\n❌ Falha na migração. Verifique as configurações do banco de dados.")
        exit(1)

