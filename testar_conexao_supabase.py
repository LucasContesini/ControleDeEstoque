#!/usr/bin/env python3
"""
Script para testar conexão com Supabase
Testa diferentes configurações para identificar qual funciona
"""

import os
import sys
import socket
import psycopg2
from urllib.parse import urlparse, quote

# Credenciais do Supabase
DB_HOST = 'db.htrghiefnoaytjmcdbuk.supabase.co'
DB_PORT_5432 = 5432
DB_PORT_6543 = 6543
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'S&mur&i77681271'

def test_dns(hostname):
    """Testa resolução DNS"""
    print(f"\n🔍 Testando DNS para {hostname}...")
    try:
        # Tentar IPv4
        ipv4 = socket.gethostbyname(hostname)
        print(f"✅ IPv4: {ipv4}")
        
        # Tentar IPv6
        try:
            ipv6 = socket.getaddrinfo(hostname, None, socket.AF_INET6)[0][4][0]
            print(f"✅ IPv6: {ipv6}")
        except:
            print(f"⚠️  IPv6: Não disponível")
        
        return True
    except Exception as e:
        print(f"❌ Erro DNS: {e}")
        return False

def test_connection(host, port, use_ssl=True, description=""):
    """Testa conexão PostgreSQL"""
    print(f"\n🔌 Testando conexão: {description}")
    print(f"   Host: {host}:{port}")
    print(f"   SSL: {use_ssl}")
    
    try:
        config = {
            'host': host,
            'port': port,
            'database': DB_NAME,
            'user': DB_USER,
            'password': DB_PASSWORD,
            'connect_timeout': 10,
        }
        
        if use_ssl:
            config['sslmode'] = 'require'
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ SUCESSO! PostgreSQL version: {version[:50]}...")
        return True
    except Exception as e:
        print(f"❌ FALHOU: {str(e)[:200]}")
        return False

def test_connection_string(connection_string, description=""):
    """Testa connection string"""
    print(f"\n🔌 Testando connection string: {description}")
    print(f"   URL: {connection_string.split('@')[0]}@***")
    
    try:
        conn = psycopg2.connect(connection_string, connect_timeout=10)
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ SUCESSO! PostgreSQL version: {version[:50]}...")
        return True
    except Exception as e:
        print(f"❌ FALHOU: {str(e)[:200]}")
        return False

def main():
    print("=" * 70)
    print("🧪 TESTE DE CONEXÃO COM SUPABASE")
    print("=" * 70)
    
    # Teste 1: DNS
    test_dns(DB_HOST)
    
    # Teste 2: Conexão direta porta 5432 com SSL
    test_connection(DB_HOST, DB_PORT_5432, use_ssl=True, description="Porta 5432 (direto) com SSL")
    
    # Teste 3: Conexão direta porta 5432 sem SSL
    test_connection(DB_HOST, DB_PORT_5432, use_ssl=False, description="Porta 5432 (direto) sem SSL")
    
    # Teste 4: Connection Pooling porta 6543 com SSL
    test_connection(DB_HOST, DB_PORT_6543, use_ssl=True, description="Porta 6543 (pooling) com SSL")
    
    # Teste 5: Connection Pooling porta 6543 sem SSL
    test_connection(DB_HOST, DB_PORT_6543, use_ssl=False, description="Porta 6543 (pooling) sem SSL")
    
    # Teste 6: Connection String porta 5432
    conn_str_5432 = f"postgresql://{DB_USER}:{quote(DB_PASSWORD)}@{DB_HOST}:{DB_PORT_5432}/{DB_NAME}?sslmode=require"
    test_connection_string(conn_str_5432, "Connection String porta 5432")
    
    # Teste 7: Connection String porta 6543
    conn_str_6543 = f"postgresql://{DB_USER}:{quote(DB_PASSWORD)}@{DB_HOST}:{DB_PORT_6543}/{DB_NAME}?sslmode=require"
    test_connection_string(conn_str_6543, "Connection String porta 6543")
    
    # Teste 8: Tentar forçar IPv4
    try:
        ipv4 = socket.gethostbyname(DB_HOST)
        print(f"\n🔌 Testando conexão direta via IPv4: {ipv4}")
        test_connection(ipv4, DB_PORT_6543, use_ssl=True, description=f"IPv4 direto {ipv4}:6543")
    except Exception as e:
        print(f"⚠️  Não foi possível obter IPv4: {e}")
    
    print("\n" + "=" * 70)
    print("✅ TESTES CONCLUÍDOS")
    print("=" * 70)

if __name__ == '__main__':
    main()

