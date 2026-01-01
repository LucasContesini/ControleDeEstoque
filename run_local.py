#!/usr/bin/env python3
"""
Script para rodar o projeto localmente com Supabase
Carrega variáveis de ambiente do arquivo env.local
"""
import os
import sys

# Carregar variáveis de ambiente do env.local
if os.path.exists('env.local'):
    print("📋 Carregando variáveis de ambiente do env.local...")
    with open('env.local', 'r') as f:
        for line in f:
            line = line.strip()
            # Ignorar comentários e linhas vazias
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Remover aspas se houver
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                os.environ[key] = value
    print("✅ Variáveis carregadas!\n")
else:
    print("⚠️  Arquivo env.local não encontrado!")
    print("   O projeto tentará usar SQLite localmente.\n")

# Importar e rodar o app
if __name__ == '__main__':
    from app import app
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🚀 Iniciando servidor Flask...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ Aplicação rodando!")
    print(f"📍 Acesse: http://localhost:{port}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("💡 Pressione Ctrl+C para parar o servidor\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)

