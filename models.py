import os
from datetime import datetime

# Detectar qual banco de dados usar baseado em variável de ambiente
# Prioriza DATABASE_URL (Supabase) se disponível, senão usa SQLite
DATABASE_URL = os.getenv('DATABASE_URL', '')
DATABASE_TYPE_ENV = os.getenv('DATABASE_TYPE', '').lower()

# Se DATABASE_URL estiver configurado, usar PostgreSQL (Supabase)
# Caso contrário, verificar DATABASE_TYPE ou usar SQLite como fallback
if DATABASE_URL:
    DATABASE_TYPE = 'postgresql'
elif DATABASE_TYPE_ENV == 'postgresql' or os.getenv('DB_HOST', ''):
    DATABASE_TYPE = 'postgresql'
else:
    DATABASE_TYPE = 'sqlite'

if DATABASE_TYPE == 'postgresql':
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    if DATABASE_URL:
        # Usar connection string se disponível (mais confiável)
        DATABASE_CONFIG = DATABASE_URL
    else:
        # Configurações do PostgreSQL via variáveis de ambiente individuais
        DATABASE_CONFIG = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'controle_estoque'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'connect_timeout': 10,  # Timeout de conexão de 10 segundos
            'sslmode': 'require'  # Requer SSL para Supabase
        }
    DATABASE = None  # Não usado para PostgreSQL
else:
    import sqlite3
    DATABASE = os.getenv('DATABASE_PATH', 'database.db')

def init_db():
    """Inicializa o banco de dados criando as tabelas necessárias"""
    if DATABASE_TYPE == 'postgresql':
        # Se DATABASE_CONFIG é string (connection string), usar diretamente
        if isinstance(DATABASE_CONFIG, str):
            conn = psycopg2.connect(DATABASE_CONFIG)
        else:
            conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        # Criar tabela se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id SERIAL PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                descricao TEXT,
                quantidade INTEGER NOT NULL DEFAULT 0,
                valor_compra DECIMAL(10, 2),
                imagem VARCHAR(500),
                especificacoes TEXT,
                data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Verificar e adicionar colunas se não existirem
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='produtos'
        """)
        colunas_existentes = [row[0] for row in cursor.fetchall()]
        
        if 'valor_compra' not in colunas_existentes:
            cursor.execute('ALTER TABLE produtos ADD COLUMN valor_compra DECIMAL(10, 2)')
        
        if 'quantidade' not in colunas_existentes:
            cursor.execute('ALTER TABLE produtos ADD COLUMN quantidade INTEGER NOT NULL DEFAULT 0')
        
        # Remover colunas antigas se existirem (migração)
        if 'quantidade_mercado_livre' in colunas_existentes:
            try:
                cursor.execute('ALTER TABLE produtos DROP COLUMN quantidade_mercado_livre')
            except:
                pass  # Ignorar se não conseguir remover
        
        if 'quantidade_shopee' in colunas_existentes:
            try:
                cursor.execute('ALTER TABLE produtos DROP COLUMN quantidade_shopee')
            except:
                pass  # Ignorar se não conseguir remover
        
        # Criar tabela de vendas (sem foreign key para preservar vendas mesmo se produto for deletado)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id SERIAL PRIMARY KEY,
                produto_id INTEGER,
                produto_titulo VARCHAR(255),
                valor_venda DECIMAL(10, 2) NOT NULL,
                valor_compra DECIMAL(10, 2) NOT NULL,
                data_venda DATE NOT NULL,
                onde_vendeu VARCHAR(20) NOT NULL CHECK (onde_vendeu IN ('mercado_livre', 'shopee')),
                observacoes TEXT,
                data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Remover foreign key se existir (para garantir que vendas não sejam deletadas)
        try:
            cursor.execute("""
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE table_name = 'vendas'
                AND constraint_type = 'FOREIGN KEY'
            """)
            constraints = cursor.fetchall()
            for constraint in constraints:
                constraint_name = constraint[0] if isinstance(constraint, tuple) else constraint.get('constraint_name', '')
                if constraint_name:
                    try:
                        cursor.execute(f'ALTER TABLE vendas DROP CONSTRAINT {constraint_name}')
                        print(f"✅ Foreign key {constraint_name} removida (vendas serão preservadas)")
                    except Exception as e:
                        print(f"⚠️  Erro ao remover foreign key: {e}")
        except Exception as e:
            print(f"⚠️  Erro ao verificar foreign keys: {e}")
        
        # Adicionar coluna produto_titulo se não existir (migração)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='vendas' AND column_name='produto_titulo'
        """)
        if not cursor.fetchone():
            cursor.execute('ALTER TABLE vendas ADD COLUMN produto_titulo VARCHAR(255)')
            # Preencher produto_titulo com dados existentes
            cursor.execute('''
                UPDATE vendas v
                SET produto_titulo = p.titulo
                FROM produtos p
                WHERE v.produto_id = p.id AND v.produto_titulo IS NULL
            ''')
        
        # Remover foreign key se existir (para garantir que vendas não sejam deletadas)
        try:
            cursor.execute("""
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE table_name = 'vendas'
                AND constraint_type = 'FOREIGN KEY'
            """)
            constraints = cursor.fetchall()
            for constraint in constraints:
                constraint_name = constraint[0] if isinstance(constraint, tuple) else constraint.get('constraint_name', '')
                if constraint_name:
                    try:
                        cursor.execute(f'ALTER TABLE vendas DROP CONSTRAINT {constraint_name}')
                        print(f"✅ Foreign key {constraint_name} removida (vendas serão preservadas)")
                    except Exception as e:
                        print(f"⚠️  Erro ao remover foreign key: {e}")
        except Exception as e:
            print(f"⚠️  Erro ao verificar foreign keys: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
    else:
        # SQLite (desenvolvimento)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                quantidade INTEGER NOT NULL DEFAULT 0,
                valor_compra REAL,
                imagem TEXT,
                especificacoes TEXT,
                data_criacao TEXT NOT NULL,
                data_atualizacao TEXT NOT NULL
            )
        ''')
        
        # Verificar colunas existentes
        cursor.execute("PRAGMA table_info(produtos)")
        colunas = [coluna[1] for coluna in cursor.fetchall()]
        
        if 'valor_compra' not in colunas:
            try:
                cursor.execute('ALTER TABLE produtos ADD COLUMN valor_compra REAL')
            except sqlite3.OperationalError:
                pass
        
        if 'quantidade' not in colunas:
            try:
                cursor.execute('ALTER TABLE produtos ADD COLUMN quantidade INTEGER NOT NULL DEFAULT 0')
            except sqlite3.OperationalError:
                pass
        
        # SQLite não suporta DROP COLUMN diretamente, então apenas ignoramos as colunas antigas
        # Elas não serão usadas e podem ser removidas manualmente se necessário
        
        # Criar tabela de vendas (sem foreign key para preservar vendas mesmo se produto for deletado)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
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
        
        # Adicionar coluna produto_titulo se não existir (migração)
        cursor.execute("PRAGMA table_info(vendas)")
        colunas = [coluna[1] for coluna in cursor.fetchall()]
        if 'produto_titulo' not in colunas:
            try:
                cursor.execute('ALTER TABLE vendas ADD COLUMN produto_titulo TEXT')
                # Preencher produto_titulo com dados existentes
                cursor.execute('''
                    UPDATE vendas 
                    SET produto_titulo = (SELECT titulo FROM produtos WHERE produtos.id = vendas.produto_id)
                    WHERE produto_titulo IS NULL AND produto_id IS NOT NULL
                ''')
            except sqlite3.OperationalError:
                pass
        
        conn.commit()
        conn.close()

def get_db():
    """Retorna uma conexão com o banco de dados"""
    if DATABASE_TYPE == 'postgresql':
        # Se DATABASE_CONFIG é string (connection string), usar diretamente
        if isinstance(DATABASE_CONFIG, str):
            conn = psycopg2.connect(DATABASE_CONFIG)
        else:
            conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    else:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

def produto_para_dict(produto):
    """Converte um produto (Row/Dict) em dicionário"""
    if DATABASE_TYPE == 'postgresql':
        # PostgreSQL retorna dict-like object
        quantidade = int(produto.get('quantidade', 0) or 0)
        return {
            'id': produto['id'],
            'titulo': produto['titulo'],
            'descricao': produto['descricao'],
            'quantidade': quantidade,
            'valor_compra': float(produto.get('valor_compra', 0) or 0),
            'imagem': produto['imagem'],
            'especificacoes': produto['especificacoes'],
            'data_criacao': produto['data_criacao'].isoformat() if produto['data_criacao'] else '',
            'data_atualizacao': produto['data_atualizacao'].isoformat() if produto['data_atualizacao'] else ''
        }
    else:
        # SQLite
        try:
            quantidade = int(produto['quantidade'] if produto['quantidade'] is not None else 0)
        except (KeyError, ValueError, TypeError):
            quantidade = 0
        
        # Obter valor_compra de forma segura (SQLite Row não tem .get())
        try:
            valor_compra = float(produto['valor_compra'] if produto['valor_compra'] is not None else 0)
        except (KeyError, ValueError, TypeError):
            valor_compra = 0.0
        
        return {
            'id': produto['id'],
            'titulo': produto['titulo'],
            'descricao': produto['descricao'],
            'quantidade': quantidade,
            'valor_compra': valor_compra,
            'imagem': produto['imagem'],
            'especificacoes': produto['especificacoes'],
            'data_criacao': produto['data_criacao'],
            'data_atualizacao': produto['data_atualizacao']
        }

def venda_para_dict(venda, produto_titulo=None):
    """Converte uma venda (Row/Dict) em dicionário"""
    if DATABASE_TYPE == 'postgresql':
        valor_venda = float(venda.get('valor_venda', 0) or 0)
        valor_compra = float(venda.get('valor_compra', 0) or 0)
        lucro = valor_venda - valor_compra
        porcentagem_lucro = (lucro / valor_compra * 100) if valor_compra > 0 else 0
        
        # Usar produto_titulo da tabela vendas se disponível, senão usar o passado como parâmetro
        titulo_final = venda.get('produto_titulo') or produto_titulo or 'Produto Deletado'
        
        return {
            'id': venda['id'],
            'produto_id': venda.get('produto_id'),  # Pode ser NULL se produto foi deletado
            'produto_titulo': titulo_final,
            'valor_venda': valor_venda,
            'valor_compra': valor_compra,
            'lucro': lucro,
            'porcentagem_lucro': round(porcentagem_lucro, 2),
            'data_venda': venda['data_venda'].strftime('%Y-%m-%d') if hasattr(venda['data_venda'], 'strftime') else str(venda['data_venda']).split('T')[0].split(' ')[0],
            'onde_vendeu': venda['onde_vendeu'],
            'observacoes': venda.get('observacoes', ''),
            'data_criacao': venda['data_criacao'].isoformat() if hasattr(venda['data_criacao'], 'isoformat') else str(venda['data_criacao'])
        }
    else:
        # SQLite
        try:
            valor_venda = float(venda['valor_venda'] if venda['valor_venda'] is not None else 0)
        except (KeyError, ValueError, TypeError):
            valor_venda = 0.0
        
        try:
            valor_compra = float(venda['valor_compra'] if venda['valor_compra'] is not None else 0)
        except (KeyError, ValueError, TypeError):
            valor_compra = 0.0
        
        lucro = valor_venda - valor_compra
        porcentagem_lucro = (lucro / valor_compra * 100) if valor_compra > 0 else 0
        
        # Usar produto_titulo da tabela vendas se disponível, senão usar o passado como parâmetro
        titulo_final = venda.get('produto_titulo') or produto_titulo or 'Produto Deletado'
        
        return {
            'id': venda['id'],
            'produto_id': venda.get('produto_id'),  # Pode ser NULL se produto foi deletado
            'produto_titulo': titulo_final,
            'valor_venda': valor_venda,
            'valor_compra': valor_compra,
            'lucro': lucro,
            'porcentagem_lucro': round(porcentagem_lucro, 2),
            'data_venda': venda['data_venda'].split('T')[0].split(' ')[0] if isinstance(venda['data_venda'], str) else str(venda['data_venda']).split('T')[0].split(' ')[0],
            'onde_vendeu': venda['onde_vendeu'],
            'observacoes': venda.get('observacoes', '') or '',
            'data_criacao': venda['data_criacao']
        }
