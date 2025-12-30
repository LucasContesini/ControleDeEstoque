import os
from datetime import datetime

# Detectar qual banco de dados usar baseado em variável de ambiente
# Use 'sqlite' para desenvolvimento ou 'postgresql' para produção
DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite').lower()

if DATABASE_TYPE == 'postgresql':
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    # Verificar se há DATABASE_URL (connection string completa)
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    
    if DATABASE_URL:
        # Se for URL interna do Railway, tentar usar variáveis individuais primeiro
        if 'railway.internal' in DATABASE_URL:
            # URL interna do Railway - usar variáveis individuais se disponíveis
            db_host = os.getenv('PGHOST') or os.getenv('DB_HOST', '')
            db_port = os.getenv('PGPORT') or os.getenv('DB_PORT', '5432')
            db_name = os.getenv('PGDATABASE') or os.getenv('DB_NAME', '')
            db_user = os.getenv('PGUSER') or os.getenv('DB_USER', '')
            db_password = os.getenv('PGPASSWORD') or os.getenv('DB_PASSWORD', '')
            
            if db_host and db_name and db_user and db_password:
                # Construir URL pública se tiver variáveis individuais
                DATABASE_CONFIG = {
                    'host': db_host,
                    'port': db_port,
                    'database': db_name,
                    'user': db_user,
                    'password': db_password,
                    'connect_timeout': 10
                }
            else:
                # Tentar usar URL interna mesmo (pode funcionar se estiver na mesma rede)
                DATABASE_CONFIG = DATABASE_URL
        else:
            # URL externa/pública - usar diretamente
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
                quantidade_mercado_livre INTEGER NOT NULL DEFAULT 0,
                quantidade_shopee INTEGER NOT NULL DEFAULT 0,
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
        
        if 'quantidade_mercado_livre' not in colunas_existentes:
            cursor.execute('ALTER TABLE produtos ADD COLUMN quantidade_mercado_livre INTEGER NOT NULL DEFAULT 0')
        
        if 'quantidade_shopee' not in colunas_existentes:
            cursor.execute('ALTER TABLE produtos ADD COLUMN quantidade_shopee INTEGER NOT NULL DEFAULT 0')
        
        # Migração: remover coluna quantidade se existir (não é mais necessária)
        if 'quantidade' in colunas_existentes:
            try:
                cursor.execute('ALTER TABLE produtos DROP COLUMN quantidade')
            except:
                pass  # Ignorar se não conseguir remover
        
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
                quantidade_mercado_livre INTEGER NOT NULL DEFAULT 0,
                quantidade_shopee INTEGER NOT NULL DEFAULT 0,
                imagem TEXT,
                especificacoes TEXT,
                data_criacao TEXT NOT NULL,
                data_atualizacao TEXT NOT NULL
            )
        ''')
        
        # Migração: adicionar colunas de quantidade por e-commerce se não existirem
        cursor.execute("PRAGMA table_info(produtos)")
        colunas = [coluna[1] for coluna in cursor.fetchall()]
        
        if 'quantidade_mercado_livre' not in colunas:
            try:
                cursor.execute('ALTER TABLE produtos ADD COLUMN quantidade_mercado_livre INTEGER NOT NULL DEFAULT 0')
            except sqlite3.OperationalError:
                pass
        
        if 'quantidade_shopee' not in colunas:
            try:
                cursor.execute('ALTER TABLE produtos ADD COLUMN quantidade_shopee INTEGER NOT NULL DEFAULT 0')
            except sqlite3.OperationalError:
                pass
        
        # Migração: remover coluna quantidade se existir (não é mais necessária)
        if 'quantidade' in colunas:
            try:
                # SQLite não suporta DROP COLUMN diretamente, precisamos recriar a tabela
                # Mas vamos apenas ignorar a coluna nas queries
                pass
            except:
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
        quantidade_ml = produto.get('quantidade_mercado_livre', 0) or 0
        quantidade_shopee = produto.get('quantidade_shopee', 0) or 0
        quantidade_total = quantidade_ml + quantidade_shopee  # Calcular total
        return {
            'id': produto['id'],
            'titulo': produto['titulo'],
            'descricao': produto['descricao'],
            'quantidade': quantidade_total,  # Calculado dinamicamente
            'quantidade_mercado_livre': quantidade_ml,
            'quantidade_shopee': quantidade_shopee,
            'imagem': produto['imagem'],
            'especificacoes': produto['especificacoes'],
            'data_criacao': produto['data_criacao'].isoformat() if produto['data_criacao'] else '',
            'data_atualizacao': produto['data_atualizacao'].isoformat() if produto['data_atualizacao'] else ''
        }
    else:
        # SQLite
        try:
            quantidade_ml = produto['quantidade_mercado_livre'] if produto['quantidade_mercado_livre'] is not None else 0
        except (KeyError, IndexError):
            quantidade_ml = 0
        
        try:
            quantidade_shopee = produto['quantidade_shopee'] if produto['quantidade_shopee'] is not None else 0
        except (KeyError, IndexError):
            quantidade_shopee = 0
        
        quantidade_total = quantidade_ml + quantidade_shopee  # Calcular total
        
        # Tentar obter quantidade da coluna antiga se existir (para compatibilidade)
        try:
            quantidade_antiga = produto.get('quantidade', None)
            if quantidade_antiga is not None:
                # Se a coluna antiga existir, usar ela, senão calcular
                quantidade_total = int(quantidade_antiga) if quantidade_antiga else quantidade_total
        except:
            pass
        
        return {
            'id': produto['id'],
            'titulo': produto['titulo'],
            'descricao': produto['descricao'],
            'quantidade': quantidade_total,  # Calculado dinamicamente
            'quantidade_mercado_livre': quantidade_ml,
            'quantidade_shopee': quantidade_shopee,
            'imagem': produto['imagem'],
            'especificacoes': produto['especificacoes'],
            'data_criacao': produto['data_criacao'],
            'data_atualizacao': produto['data_atualizacao']
        }
