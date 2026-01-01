"""
Configurações centralizadas do projeto
Todas as configurações sensíveis vêm de variáveis de ambiente
"""
import os

# ============================================================================
# VARIÁVEIS DE AMBIENTE (Todas as configurações)
# ============================================================================

# URL do projeto Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', '')

# Configurações do banco de dados PostgreSQL
# IMPORTANTE: Vercel é IPv4-only! Use Session Pooler do Supabase.
# No Supabase Dashboard → Settings → Database → Connection Pooling
# Copie a connection string do Session Pooler ou use as variáveis abaixo
DB_HOST = os.getenv('DB_HOST', '')  # Host do Session Pooler (ex: aws-0-us-west-2.pooler.supabase.com)
DB_PORT = os.getenv('DB_PORT', '5432')  # Porta do Session Pooler (geralmente 5432)
DB_NAME = os.getenv('DB_NAME', 'postgres')  # Nome do banco (geralmente postgres)
DB_USER = os.getenv('DB_USER', '')  # User do Session Pooler (formato: postgres.PROJECT_REF)
DB_PASSWORD = os.getenv('DB_PASSWORD', '')  # Senha do banco

# Connection string completa (opcional - se usar, não precisa das variáveis acima)
DATABASE_URL = os.getenv('DATABASE_URL', '')

# Nome do bucket no Supabase Storage
BUCKET_NAME = os.getenv('BUCKET_NAME', 'Controle de Estoque')

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

