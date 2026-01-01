"""
Configurações centralizadas do projeto
Valores hardcoded específicos do projeto Supabase
Apenas credenciais sensíveis vêm de variáveis de ambiente
"""
import os

# ============================================================================
# CONFIGURAÇÕES DO SUPABASE (Hardcoded - específicas do projeto)
# ============================================================================

# URL do projeto Supabase
SUPABASE_URL = 'https://htrghiefnoaytjmcdbuk.supabase.co'

# Configurações do banco de dados PostgreSQL
DB_HOST = 'db.htrghiefnoaytjmcdbuk.supabase.co'
DB_PORT = '6543'  # Porta de connection pooling (mais confiável no Vercel)
DB_NAME = 'postgres'  # Nome padrão do banco no Supabase
DB_USER = 'postgres'  # Usuário padrão do Supabase

# Nome do bucket no Supabase Storage
BUCKET_NAME = 'Controle de Estoque'

# ============================================================================
# VARIÁVEIS DE AMBIENTE (Apenas credenciais sensíveis)
# ============================================================================

# Senha do banco de dados (OBRIGATÓRIA em produção)
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# Chaves do Supabase (OBRIGATÓRIAS em produção)
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')  # Chave anon (pública)
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', '')  # Chave service_role (secreta)

# ============================================================================
# CONFIGURAÇÕES AUTOMÁTICAS
# ============================================================================

# Detectar se está no Vercel
IS_VERCEL = os.getenv('VERCEL', '') != '' or os.getenv('VERCEL_ENV', '') != ''

# Tipo de banco: 'postgresql' em produção (Vercel), 'sqlite' em desenvolvimento
DATABASE_TYPE = 'postgresql' if IS_VERCEL or os.getenv('DATABASE_TYPE', '').lower() == 'postgresql' else 'sqlite'

# ============================================================================
# VALIDAÇÃO
# ============================================================================

def validar_configuracao():
    """Valida se as configurações obrigatórias estão presentes"""
    erros = []
    
    if DATABASE_TYPE == 'postgresql':
        if not DB_PASSWORD:
            erros.append("DB_PASSWORD não configurada (obrigatória para PostgreSQL)")
    
    if not SUPABASE_KEY:
        erros.append("SUPABASE_KEY não configurada (obrigatória para Storage)")
    
    if not SUPABASE_SERVICE_KEY:
        erros.append("SUPABASE_SERVICE_KEY não configurada (obrigatória para upload de imagens)")
    
    if erros:
        raise ValueError("Erros de configuração:\n" + "\n".join(f"  - {e}" for e in erros))
    
    return True

