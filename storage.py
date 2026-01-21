"""
Módulo para gerenciar armazenamento de imagens no Supabase Storage
"""
import os
from supabase import create_client, Client
from werkzeug.utils import secure_filename
from datetime import datetime

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')  # Chave anon (para operações normais)
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', '')  # Chave service_role (para admin)
BUCKET_NAME = 'Controle de Estoque'

# Cliente Supabase (será inicializado quando necessário)
_supabase_client: Client = None

def get_supabase_client(use_service_key=False):
    """Retorna o cliente Supabase"""
    global _supabase_client
    # Se precisar de service key, criar cliente separado
    if use_service_key:
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_SERVICE_KEY devem estar configurados")
        url = SUPABASE_URL.rstrip('/') + '/'
        return create_client(url, SUPABASE_SERVICE_KEY)
    
    # Cliente normal com anon key
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
        # Garantir que a URL termine com /
        url = SUPABASE_URL.rstrip('/') + '/'
        _supabase_client = create_client(url, SUPABASE_KEY)
    return _supabase_client

def usar_storage_cloud():
    """Verifica se deve usar storage em nuvem"""
    return bool(SUPABASE_URL and SUPABASE_KEY)

def upload_imagem_cloud(file, filename):
    """
    Faz upload de uma imagem para o Supabase Storage
    Retorna a URL pública da imagem
    """
    try:
        # Usar service key para upload (tem permissões administrativas)
        # Se não tiver service key, usar anon key
        supabase = get_supabase_client(use_service_key=True) if SUPABASE_SERVICE_KEY else get_supabase_client()
        
        # Ler o arquivo
        file_content = file.read()
        file.seek(0)  # Resetar posição do arquivo
        
        # Determinar content type
        content_type = file.content_type or 'image/jpeg'
        if filename.lower().endswith('.png'):
            content_type = 'image/png'
        elif filename.lower().endswith('.gif'):
            content_type = 'image/gif'
        elif filename.lower().endswith('.webp'):
            content_type = 'image/webp'
        
        # Fazer upload (tentar fazer upload diretamente, sem verificar bucket)
        try:
            response = supabase.storage.from_(BUCKET_NAME).upload(
                filename,
                file_content,
                file_options={"content-type": content_type, "upsert": "true"}
            )
        except Exception as upload_error:
            # Se der erro, tentar sem upsert
            response = supabase.storage.from_(BUCKET_NAME).upload(
                filename,
                file_content,
                file_options={"content-type": content_type}
            )
        
        # Obter URL pública (pode usar anon key para isso)
        url = supabase.storage.from_(BUCKET_NAME).get_public_url(filename)
        
        return url
    except Exception as e:
        raise Exception(f"Erro ao fazer upload para Supabase: {str(e)}")

def deletar_imagem_cloud(filename):
    """Deleta uma imagem do Supabase Storage"""
    try:
        # Se for URL externa (Unsplash), não deletar
        if filename.startswith('https://source.unsplash.com') or filename.startswith('http://source.unsplash.com'):
            return False
        
        # Usar service key para deletar (tem permissões administrativas)
        supabase = get_supabase_client(use_service_key=True) if SUPABASE_SERVICE_KEY else get_supabase_client()
        
        # Extrair apenas o nome do arquivo da URL se for uma URL completa do Supabase
        if filename.startswith('http'):
            # Se for URL do Supabase, extrair o nome do arquivo
            if 'supabase.co' in filename or 'storage.supabase.co' in filename:
                # URL do Supabase: https://xxx.supabase.co/storage/v1/object/public/bucket/filename
                filename = filename.split('/')[-1]
            else:
                # URL externa que não é do Supabase, não deletar
                return False
        
        supabase.storage.from_(BUCKET_NAME).remove([filename])
        return True
    except Exception as e:
        print(f"Erro ao deletar imagem do Supabase: {e}")
        return False

def criar_bucket_se_nao_existir():
    """Cria o bucket no Supabase Storage se não existir"""
    try:
        # Usar service key para operações administrativas
        supabase = get_supabase_client(use_service_key=True) if SUPABASE_SERVICE_KEY else get_supabase_client()
        
        # Listar buckets existentes
        buckets = supabase.storage.list_buckets()
        bucket_names = [b.name for b in buckets]
        
        if BUCKET_NAME not in bucket_names:
            # Criar bucket público para que as imagens sejam acessíveis
            supabase.storage.create_bucket(
                BUCKET_NAME,
                options={"public": True}
            )
            print(f"✅ Bucket '{BUCKET_NAME}' criado no Supabase Storage")
        else:
            print(f"✅ Bucket '{BUCKET_NAME}' encontrado")
    except Exception as e:
        print(f"⚠️  Erro ao verificar/criar bucket: {e}")
        print(f"   O bucket '{BUCKET_NAME}' deve existir e estar público no painel do Supabase")

