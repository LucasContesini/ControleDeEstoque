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
    
    # Verificar se deve usar connection pooling (porta 6543)
    # Connection pooling é mais confiável em ambientes serverless como Vercel
    USE_POOLING = os.getenv('USE_CONNECTION_POOLING', 'false').lower() == 'true'
    POOLING_PORT = '6543'
    
    if DATABASE_URL:
        # URL externa/pública (Supabase) - garantir SSL
        # Se não tiver sslmode na URL, adicionar
        if 'sslmode=' not in DATABASE_URL:
            separator = '&' if '?' in DATABASE_URL else '?'
            DATABASE_CONFIG = f"{DATABASE_URL}{separator}sslmode=require"
        else:
            DATABASE_CONFIG = DATABASE_URL
        
        # Se usar pooling e a URL não especificar porta, usar porta 6543
        if USE_POOLING and ':6543' not in DATABASE_CONFIG and ':5432' not in DATABASE_CONFIG:
            # Substituir porta padrão por 6543
            if '@' in DATABASE_CONFIG and '/' in DATABASE_CONFIG:
                parts = DATABASE_CONFIG.split('@')
                if len(parts) == 2:
                    host_part = parts[1].split('/')[0]
                    if ':' not in host_part:
                        # Adicionar porta de pooling
                        DATABASE_CONFIG = DATABASE_CONFIG.replace(f"@{host_part}", f"@{host_part}:{POOLING_PORT}")
    else:
        # Configurações do PostgreSQL via variáveis de ambiente individuais
        db_port = os.getenv('DB_PORT', POOLING_PORT if USE_POOLING else '5432')
        DATABASE_CONFIG = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': db_port,
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
            # Garantir que SSL está configurado na connection string
            conn = psycopg2.connect(
                DATABASE_CONFIG,
                connect_timeout=10
            )
        else:
            # Garantir SSL e timeout quando usar dict
            config = dict(DATABASE_CONFIG)
            if 'sslmode' not in config:
                config['sslmode'] = 'require'
            if 'connect_timeout' not in config:
                config['connect_timeout'] = 10
            conn = psycopg2.connect(**config)
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
        try:
            # Se DATABASE_CONFIG é string (connection string), usar diretamente
            if isinstance(DATABASE_CONFIG, str):
                # Garantir que SSL está configurado na connection string
                conn = psycopg2.connect(
                    DATABASE_CONFIG,
                    connect_timeout=10
                )
            else:
                # Garantir SSL e timeout quando usar dict
                config = dict(DATABASE_CONFIG)
                if 'sslmode' not in config:
                    config['sslmode'] = 'require'
                if 'connect_timeout' not in config:
                    config['connect_timeout'] = 10
                conn = psycopg2.connect(**config)
            return conn
        except psycopg2.OperationalError as e:
            # Melhorar mensagem de erro com informações úteis
            error_msg = str(e)
            if 'Cannot assign requested address' in error_msg or 'Network is unreachable' in error_msg:
                # Tentar connection pooling como fallback se não estiver usando
                USE_POOLING = os.getenv('USE_CONNECTION_POOLING', 'false').lower() == 'true'
                if not USE_POOLING:
                    suggestion = (
                        f"\n\n💡 Dica: Tente usar Connection Pooling do Supabase (porta 6543). "
                        f"Adicione no Vercel:\n"
                        f"USE_CONNECTION_POOLING=true\n"
                        f"DB_PORT=6543\n\n"
                        f"Ou use DATABASE_URL com porta 6543:\n"
                        f"DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:6543/postgres?sslmode=require"
                    )
                else:
                    suggestion = ""
                
                raise Exception(
                    f"Erro de conexão de rede com o banco de dados. "
                    f"Verifique:\n"
                    f"1. Se o Supabase permite conexões externas (Settings → Database → Network Restrictions)\n"
                    f"2. Se as variáveis de ambiente estão configuradas corretamente no Vercel\n"
                    f"3. Se o host/porta estão corretos\n"
                    f"4. Tente usar Connection Pooling (porta 6543) em vez de conexão direta (porta 5432)\n"
                    f"Erro original: {error_msg}{suggestion}"
                )
            raise Exception(f"Erro ao conectar ao banco de dados: {error_msg}")
    else:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

def produto_para_dict(produto):
    """Converte um produto (Row/Dict) em dicionário"""
    if DATABASE_TYPE == 'postgresql':
        # PostgreSQL retorna dict-like object
        quantidade_ml = int(produto.get('quantidade_mercado_livre', 0) or 0)
        quantidade_shopee = int(produto.get('quantidade_shopee', 0) or 0)
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
            quantidade_ml = int(produto['quantidade_mercado_livre'] if produto['quantidade_mercado_livre'] is not None else 0)
        except (KeyError, IndexError):
            quantidade_ml = 0
        
        try:
            quantidade_shopee = int(produto['quantidade_shopee'] if produto['quantidade_shopee'] is not None else 0)
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
