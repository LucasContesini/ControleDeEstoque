"""Helper para compatibilidade entre SQLite e PostgreSQL"""
from models import DATABASE_TYPE

def get_placeholder():
    """Retorna o placeholder correto para queries"""
    return '%s' if DATABASE_TYPE == 'postgresql' else '?'

def get_cursor(conn):
    """Retorna cursor apropriado para o banco de dados"""
    if DATABASE_TYPE == 'postgresql':
        from psycopg2.extras import RealDictCursor
        return conn.cursor(cursor_factory=RealDictCursor)
    return conn.cursor()

