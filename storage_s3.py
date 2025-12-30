"""
Módulo alternativo para usar Supabase Storage via S3 API
Use este se preferir usar as credenciais S3 diretamente
"""
import os
import boto3
from botocore.client import Config
from werkzeug.utils import secure_filename

# Configurações S3 do Supabase
S3_ENDPOINT = os.getenv('SUPABASE_S3_ENDPOINT', '')
S3_ACCESS_KEY = os.getenv('SUPABASE_S3_ACCESS_KEY', '')
S3_SECRET_KEY = os.getenv('SUPABASE_S3_SECRET_KEY', '')
S3_REGION = os.getenv('SUPABASE_S3_REGION', 'us-west-2')
BUCKET_NAME = 'Controle de Estoque'

# Cliente S3 (será inicializado quando necessário)
_s3_client = None

def get_s3_client():
    """Retorna o cliente S3 configurado para Supabase"""
    global _s3_client
    if _s3_client is None:
        if not all([S3_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY]):
            raise ValueError("Credenciais S3 do Supabase devem estar configuradas")
        
        # Limpar endpoint (remover /storage/v1/s3 se presente)
        endpoint = S3_ENDPOINT.rstrip('/')
        if '/storage/v1/s3' in endpoint:
            endpoint = endpoint.split('/storage/v1/s3')[0]
        endpoint = endpoint.rstrip('/')
        
        _s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            region_name=S3_REGION,
            config=Config(
                signature_version='s3v4',
                s3={
                    'addressing_style': 'path',
                    'payload_signing_enabled': False
                }
            )
        )
    return _s3_client

def usar_storage_s3():
    """Verifica se deve usar storage S3"""
    return bool(S3_ENDPOINT and S3_ACCESS_KEY and S3_SECRET_KEY)

def upload_imagem_s3(file, filename):
    """
    Faz upload de uma imagem para o Supabase Storage via S3
    Retorna a URL pública da imagem
    """
    try:
        s3 = get_s3_client()
        
        # Verificar se o bucket existe
        try:
            s3.head_bucket(Bucket=BUCKET_NAME)
        except Exception:
            raise Exception(f"Bucket '{BUCKET_NAME}' não encontrado. Crie o bucket no painel do Supabase.")
        
        # Ler o arquivo
        file_content = file.read()
        file.seek(0)
        
        # Determinar content type
        content_type = file.content_type or 'image/jpeg'
        if filename.lower().endswith('.png'):
            content_type = 'image/png'
        elif filename.lower().endswith('.gif'):
            content_type = 'image/gif'
        elif filename.lower().endswith('.webp'):
            content_type = 'image/webp'
        
        # Fazer upload (sem ACL, pois o bucket já é público)
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=file_content,
            ContentType=content_type
        )
        
        # Construir URL pública do Supabase Storage
        # Formato: https://[project].supabase.co/storage/v1/object/public/[bucket]/[file]
        # Extrair project ID do endpoint
        endpoint_clean = S3_ENDPOINT.replace('https://', '').replace('http://', '').rstrip('/')
        endpoint_parts = endpoint_clean.split('.')
        project_id = endpoint_parts[0]
        url = f"https://{project_id}.supabase.co/storage/v1/object/public/{BUCKET_NAME}/{filename}"
        
        return url
    except Exception as e:
        raise Exception(f"Erro ao fazer upload via S3: {str(e)}")

def deletar_imagem_s3(filename):
    """Deleta uma imagem do Supabase Storage via S3"""
    try:
        s3 = get_s3_client()
        
        # Extrair apenas o nome do arquivo da URL se for uma URL completa
        if filename.startswith('http'):
            filename = filename.split('/')[-1]
        
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return True
    except Exception as e:
        print(f"Erro ao deletar imagem via S3: {e}")
        return False

