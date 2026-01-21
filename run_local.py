#!/usr/bin/env python3
"""
Script para rodar o projeto localmente usando Supabase
Carrega variáveis de ambiente do arquivo env.local
"""

import os
import sys
from pathlib import Path

# Carregar variáveis de ambiente do arquivo env.local
env_file = Path(__file__).parent / 'env.local'
if env_file.exists():
    print("📋 Carregando variáveis de ambiente de env.local...")
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Ignorar comentários e linhas vazias
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remover aspas se houver
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key] = value
    print("✅ Variáveis de ambiente carregadas!")
else:
    print("⚠️  Arquivo env.local não encontrado!")
    print("   Criando arquivo de exemplo...")
    # Criar arquivo de exemplo
    with open(env_file, 'w') as f:
        f.write("""# Configuração Local - Supabase
# Configure suas credenciais do Supabase aqui

DATABASE_URL=postgresql://user:password@host:port/database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key
BUCKET_NAME=Controle de Estoque
""")
    print(f"   Arquivo criado: {env_file}")
    print("   Configure as variáveis e execute novamente.")
    sys.exit(1)

# Verificar se DATABASE_URL está configurado
if not os.getenv('DATABASE_URL'):
    print("❌ DATABASE_URL não configurado!")
    print("   Configure DATABASE_URL no arquivo env.local")
    sys.exit(1)

# Importar e rodar o app
print("🚀 Iniciando servidor Flask...")
print("📍 Acesse: http://localhost:5001")
print("💡 Pressione Ctrl+C para parar\n")

from app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)

