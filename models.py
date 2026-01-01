import os
from datetime import datetime
from config import (
    DATABASE_TYPE, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,
    IS_VERCEL
)

if DATABASE_TYPE == 'postgresql':
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    # Verificar se há DATABASE_URL (connection string completa) - opcional
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    
    if DATABASE_URL:
        # URL externa/pública (Supabase) - garantir SSL
        # Se não tiver sslmode na URL, adicionar
        if 'sslmode=' not in DATABASE_URL:
            separator = '&' if '?' in DATABASE_URL else '?'
            DATABASE_CONFIG = f"{DATABASE_URL}{separator}sslmode=require"
        else:
            DATABASE_CONFIG = DATABASE_URL
        
        # Garantir que está usando porta de pooling (6543)
        if ':5432' in DATABASE_CONFIG:
            DATABASE_CONFIG = DATABASE_CONFIG.replace(':5432', ':6543')
    else:
        # Configurações do PostgreSQL usando valores do config.py
        DATABASE_CONFIG = {
            'host': DB_HOST,
            'port': DB_PORT,  # Já vem como '6543' do config.py
            'database': DB_NAME,
            'user': DB_USER,
            'password': DB_PASSWORD,
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
                categoria VARCHAR(100),
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
        
        if 'categoria' not in colunas_existentes:
            cursor.execute('ALTER TABLE produtos ADD COLUMN categoria VARCHAR(100)')
        
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
                categoria TEXT,
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
        
        if 'categoria' not in colunas:
            try:
                cursor.execute('ALTER TABLE produtos ADD COLUMN categoria TEXT')
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
        import socket
        
        # No Vercel, sempre tentar IPv4 primeiro para evitar problemas com IPv6
        if IS_VERCEL and isinstance(DATABASE_CONFIG, dict):
            host = DATABASE_CONFIG.get('host', '')
            if host and 'supabase.co' in host:
                try:
                    # Resolver IPv4 antes de tentar conectar
                    ipv4 = socket.gethostbyname(host)
                    config_ipv4 = dict(DATABASE_CONFIG)
                    config_ipv4['host'] = ipv4
                    if 'sslmode' not in config_ipv4:
                        config_ipv4['sslmode'] = 'require'
                    if 'connect_timeout' not in config_ipv4:
                        config_ipv4['connect_timeout'] = 10
                    
                    # Tentar conectar com IPv4 primeiro
                    try:
                        conn = psycopg2.connect(**config_ipv4)
                        return conn
                    except psycopg2.OperationalError:
                        # Se IPv4 falhar, tentar com hostname mesmo
                        pass
                except socket.gaierror:
                    # Se não conseguir resolver IPv4, continuar com hostname
                    pass
        
        # Tentar conexão normal (ou se não for Vercel)
        attempts = []
        try:
            if isinstance(DATABASE_CONFIG, str):
                conn = psycopg2.connect(DATABASE_CONFIG, connect_timeout=10)
            else:
                config = dict(DATABASE_CONFIG)
                if 'sslmode' not in config:
                    config['sslmode'] = 'require'
                if 'connect_timeout' not in config:
                    config['connect_timeout'] = 10
                conn = psycopg2.connect(**config)
            return conn
        except psycopg2.OperationalError as e:
            error_msg = str(e)
            attempts.append(f"Tentativa 1 (normal): {error_msg[:100]}")
            
            # Se erro for IPv6 ou "Cannot assign requested address", tentar forçar IPv4
            if 'Cannot assign requested address' in error_msg or '2600:' in error_msg or 'Network is unreachable' in error_msg:
                # Abordagem 2: Tentar resolver IPv4 e conectar diretamente
                try:
                    if isinstance(DATABASE_CONFIG, dict):
                        host = DATABASE_CONFIG.get('host', '')
                        if host and 'supabase.co' in host:
                            # Resolver IPv4
                            ipv4 = socket.gethostbyname(host)
                            config_ipv4 = dict(DATABASE_CONFIG)
                            config_ipv4['host'] = ipv4
                            if 'sslmode' not in config_ipv4:
                                config_ipv4['sslmode'] = 'require'
                            if 'connect_timeout' not in config_ipv4:
                                config_ipv4['connect_timeout'] = 10
                            
                            conn = psycopg2.connect(**config_ipv4)
                            return conn
                except Exception as e2:
                    attempts.append(f"Tentativa 2 (IPv4 direto): {str(e2)[:100]}")
            
            # Se todas as tentativas falharam, retornar erro detalhado
            current_port = DATABASE_CONFIG.get('port', '?') if isinstance(DATABASE_CONFIG, dict) else '?'
            
            suggestion = ""
            if IS_VERCEL:
                suggestion = (
                    f"\n\n💡 O Vercel pode ter problemas com IPv6.\n"
                    f"O código já tenta IPv4 automaticamente, mas se o problema persistir:\n"
                    f"1. Verifique se o Supabase permite conexões externas\n"
                    f"2. Tente usar DATABASE_URL com IPv4 resolvido manualmente\n"
                    f"3. Verifique os logs do Vercel para mais detalhes"
                )
            
            raise Exception(
                f"Erro ao conectar ao banco de dados.\n"
                f"Tentativas realizadas:\n" + "\n".join(f"  - {a}" for a in attempts) + "\n\n"
                f"Verifique:\n"
                f"1. Se o Supabase permite conexões externas (Settings → Database → Network Restrictions)\n"
                f"2. Se as variáveis de ambiente estão configuradas no Vercel\n"
                f"3. Se está usando porta 6543 (pooling) em vez de 5432 (direto)\n"
                f"4. Porta atual configurada: {current_port}\n"
                f"Erro original: {error_msg}{suggestion}"
            )
        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {str(e)}")
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
            'categoria': produto.get('categoria', ''),
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
            'categoria': produto.get('categoria', '') if len(produto) > 8 else '',
            'quantidade': quantidade_total,  # Calculado dinamicamente
            'quantidade_mercado_livre': quantidade_ml,
            'quantidade_shopee': quantidade_shopee,
            'imagem': produto['imagem'],
            'especificacoes': produto['especificacoes'],
            'data_criacao': produto['data_criacao'],
            'data_atualizacao': produto['data_atualizacao']
        }
