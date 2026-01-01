"""
Módulo para gerenciar armazenamento de imagens no Supabase Storage
"""
import os
import requests
from werkzeug.utils import secure_filename
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY, BUCKET_NAME

# Tentar importar biblioteca Supabase (opcional)
try:
    from supabase import create_client, Client
    SUPABASE_LIB_AVAILABLE = True
except ImportError:
    SUPABASE_LIB_AVAILABLE = False

# Cliente Supabase (será inicializado quando necessário)
_supabase_client: Client = None
_supabase_service_client: Client = None

def get_supabase_client(use_service_key=False):
    """Retorna o cliente Supabase"""
    global _supabase_client, _supabase_service_client
    # Se precisar de service key, criar cliente separado
    if use_service_key:
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_SERVICE_KEY devem estar configurados")
        # Usar cliente em cache se já existir
        if _supabase_service_client is None:
            url = SUPABASE_URL.rstrip('/')
            # Biblioteca Supabase aceita URL com ou sem barra final
            # Funciona com chaves sb_secret_ e JWT (eyJ...)
            try:
                # Tentar criar cliente - a biblioteca supabase-py deve suportar ambas as chaves
                _supabase_service_client = create_client(url, SUPABASE_SERVICE_KEY)
            except Exception as e:
                error_str = str(e)
                # Se for erro de chave inválida, tentar dar mais contexto
                if "Invalid API key" in error_str or "invalid" in error_str.lower():
                    # Verificar se a chave parece válida
                    if SUPABASE_SERVICE_KEY.startswith('sb_secret_'):
                        # Chave sb_secret_ - a biblioteca deveria suportar, mas pode haver problema
                        raise ValueError(f"Erro ao criar cliente Supabase com chave sb_secret_: {error_str}. Verifique se a chave está correta e se a biblioteca supabase está atualizada (pip install --upgrade supabase).")
                    elif SUPABASE_SERVICE_KEY.startswith('eyJ'):
                        # Chave JWT - deveria funcionar
                        raise ValueError(f"Erro ao criar cliente Supabase com chave JWT: {error_str}. Verifique se SUPABASE_URL e SUPABASE_SERVICE_KEY estão corretos.")
                    else:
                        # Chave em formato desconhecido
                        raise ValueError(f"Formato de chave desconhecido. Use chaves sb_secret_ ou JWT (eyJ...). Erro: {error_str}")
                else:
                    raise ValueError(f"Erro ao criar cliente Supabase com service key: {error_str}. Verifique se SUPABASE_URL e SUPABASE_SERVICE_KEY estão corretos.")
        return _supabase_service_client
    
    # Cliente normal com anon key
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
        url = SUPABASE_URL.rstrip('/')
        # Biblioteca Supabase não precisa de barra final
        _supabase_client = create_client(url, SUPABASE_KEY)
    return _supabase_client

def usar_storage_cloud():
    """Verifica se deve usar storage em nuvem"""
    # Verificar se todas as variáveis necessárias estão configuradas
    return bool(SUPABASE_URL and SUPABASE_KEY and SUPABASE_SERVICE_KEY)

def upload_imagem_cloud(file, filename):
    """
    Faz upload de uma imagem para o Supabase Storage
    Retorna a URL pública da imagem
    """
    try:
        # IMPORTANTE: API REST do Supabase Storage NÃO aceita chaves sb_secret_
        # Apenas chaves JWT (eyJ...) funcionam com API REST
        # Para chaves sb_secret_, DEVEMOS usar a biblioteca Supabase
        
        # Se a chave for sb_secret_, usar biblioteca (única opção)
        if SUPABASE_SERVICE_KEY and SUPABASE_SERVICE_KEY.startswith('sb_secret_'):
            if SUPABASE_LIB_AVAILABLE and SUPABASE_URL:
                return upload_via_library(file, filename)
            else:
                raise Exception("Chaves sb_secret_ requerem a biblioteca Supabase Python. Instale: pip install supabase")
        
        # Para chaves JWT (eyJ...), tentar biblioteca primeiro, depois API REST
        if SUPABASE_LIB_AVAILABLE and SUPABASE_URL and SUPABASE_SERVICE_KEY:
            try:
                return upload_via_library(file, filename)
            except Exception as lib_error:
                # Se biblioteca falhar e for JWT, tentar API REST como fallback
                if SUPABASE_SERVICE_KEY.startswith('eyJ'):
                    try:
                        return upload_via_rest_api(file, filename)
                    except:
                        raise lib_error
                else:
                    raise lib_error
        
        # Se não tiver biblioteca, tentar API REST (só funciona com JWT)
        if SUPABASE_URL and SUPABASE_SERVICE_KEY:
            if SUPABASE_SERVICE_KEY.startswith('eyJ'):
                return upload_via_rest_api(file, filename)
            else:
                raise Exception("Biblioteca Supabase não disponível e API REST requer chaves JWT (eyJ...). Instale a biblioteca: pip install supabase")
        
        raise Exception("Nenhum método de upload disponível")
    except Exception as e:
        error_msg = str(e)
        # Melhorar mensagem de erro para chaves inválidas
        if "Invalid API key" in error_msg or "invalid" in error_msg.lower() or "401" in error_msg or "403" in error_msg:
            raise Exception(f"Chave de API inválida ou sem permissão. Verifique se SUPABASE_SERVICE_KEY está correta no Vercel Dashboard. A chave deve ser a service_role key do Supabase Dashboard → Settings → API. Erro original: {error_msg}")
        raise Exception(f"Erro ao fazer upload para Supabase: {error_msg}")

def upload_via_rest_api(file, filename):
    """Upload usando API REST diretamente (compatível com chaves sb_secret_ e JWT)"""
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
    
    # URL da API de Storage do Supabase
    url_base = SUPABASE_URL.rstrip('/')
    upload_url = f"{url_base}/storage/v1/object/{BUCKET_NAME}/{filename}"
    
    # Headers - tentar com ambas as chaves (sb_secret_ e JWT)
    service_key = SUPABASE_SERVICE_KEY
    headers = {
        "Content-Type": content_type,
        "x-upsert": "true"  # Permite sobrescrever arquivo existente
    }
    
    # Para chaves sb_secret_, usar formato diferente
    if service_key.startswith('sb_secret_'):
        # Chaves sb_secret_ podem precisar de formato diferente
        # Tentar com Authorization Bearer primeiro
        headers["Authorization"] = f"Bearer {service_key}"
    elif service_key.startswith('eyJ'):
        # Chaves JWT tradicionais
        headers["Authorization"] = f"Bearer {service_key}"
    else:
        # Tentar como Bearer de qualquer forma
        headers["Authorization"] = f"Bearer {service_key}"
    
    # Fazer upload
    response = requests.put(upload_url, data=file_content, headers=headers)
    
    if response.status_code not in [200, 201]:
        error_detail = response.text
        # Se falhar com sb_secret_, pode ser que precise usar apikey header
        if service_key.startswith('sb_secret_') and response.status_code in [401, 403]:
            # Tentar com header apikey em vez de Authorization
            headers_alt = {
                "apikey": service_key,
                "Authorization": f"Bearer {service_key}",
                "Content-Type": content_type,
                "x-upsert": "true"
            }
            response = requests.put(upload_url, data=file_content, headers=headers_alt)
            if response.status_code not in [200, 201]:
                error_detail = response.text
                raise Exception(f"Erro ao fazer upload: {response.status_code} - {error_detail}")
        else:
            raise Exception(f"Erro ao fazer upload: {response.status_code} - {error_detail}")
    
    # Construir URL pública
    public_url = f"{url_base}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
    return public_url

def upload_via_library(file, filename):
    """Upload usando biblioteca Supabase"""
    # Usar service key para upload (tem permissões administrativas)
    try:
        supabase = get_supabase_client(use_service_key=True) if SUPABASE_SERVICE_KEY else get_supabase_client()
    except Exception as e:
        # Se falhar ao criar cliente, tentar criar diretamente sem cache
        if SUPABASE_SERVICE_KEY:
            url = SUPABASE_URL.rstrip('/')
            try:
                supabase = create_client(url, SUPABASE_SERVICE_KEY)
            except Exception as e2:
                raise Exception(f"Erro ao criar cliente Supabase: {str(e2)}. Verifique se SUPABASE_URL e SUPABASE_SERVICE_KEY estão corretos.")
        else:
            raise e
    
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
    
    # Fazer upload
    try:
        response = supabase.storage.from_(BUCKET_NAME).upload(
            filename,
            file_content,
            file_options={"content-type": content_type, "upsert": "true"}
        )
    except Exception as upload_error:
        # Se der erro, tentar sem upsert
        try:
            response = supabase.storage.from_(BUCKET_NAME).upload(
                filename,
                file_content,
                file_options={"content-type": content_type}
            )
        except Exception:
            # Se ainda falhar, levantar o erro original
            raise upload_error
    
    # Obter URL pública
    url = supabase.storage.from_(BUCKET_NAME).get_public_url(filename)
    return url

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

