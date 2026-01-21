from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
import requests
from datetime import datetime
from models import init_db, get_db, produto_para_dict, venda_para_dict, DATABASE_TYPE
from db_helper import get_placeholder, get_cursor

# Tentar importar storage (opcional)
STORAGE_CLOUD_DISPONIVEL = False
USAR_S3 = False
upload_imagem_cloud = None
deletar_imagem_cloud = None
criar_bucket_se_nao_existir = None

# Tentar usar API REST primeiro (mais confiável)
try:
    from storage import usar_storage_cloud, upload_imagem_cloud, deletar_imagem_cloud, criar_bucket_se_nao_existir
    if usar_storage_cloud():
        STORAGE_CLOUD_DISPONIVEL = True
        USAR_S3 = False
        print("✅ Usando Supabase Storage via API REST")
except (ImportError, Exception) as e:
    # Se API REST não funcionar, tentar S3 como fallback
    try:
        from storage_s3 import usar_storage_s3, upload_imagem_s3, deletar_imagem_s3
        if usar_storage_s3():
            STORAGE_CLOUD_DISPONIVEL = True
            USAR_S3 = True
            upload_imagem_cloud = upload_imagem_s3
            deletar_imagem_cloud = deletar_imagem_s3
            criar_bucket_se_nao_existir = lambda: None  # Bucket já existe
            print("✅ Usando Supabase Storage via S3 (fallback)")
    except (ImportError, Exception):
        pass

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Configurar Flask para retornar JSON em caso de erro
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Criar diretório de uploads se não existir (fallback para armazenamento local)
# No Vercel, não podemos criar diretórios, então apenas tenta
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
except (OSError, PermissionError):
    pass  # No Vercel, usamos apenas Supabase Storage

# Inicialização lazy do banco de dados (não inicializar na importação)
# Será inicializado na primeira requisição
_db_initialized = False

def ensure_db_initialized():
    """Garante que o banco de dados está inicializado"""
    global _db_initialized
    if not _db_initialized:
        try:
            init_db()
            _db_initialized = True
        except Exception as e:
            error_msg = f"Erro ao conectar ao banco de dados: {str(e)}"
            print(f"⚠️  {error_msg}")
            # Levanta exceção para que a rota possa tratar e retornar JSON
            raise Exception(error_msg)

# Inicialização lazy do Supabase Storage (não inicializar na importação)
# Será inicializado na primeira requisição que precisar de upload
_storage_initialized = False

def ensure_storage_initialized():
    """Garante que o Supabase Storage está inicializado"""
    global _storage_initialized
    if not _storage_initialized and STORAGE_CLOUD_DISPONIVEL:
        try:
            if criar_bucket_se_nao_existir and callable(criar_bucket_se_nao_existir):
                criar_bucket_se_nao_existir()
            if not USAR_S3:
                print("✅ Supabase Storage configurado para imagens (API REST)")
            else:
                print("✅ Supabase Storage configurado para imagens (S3)")
            _storage_initialized = True
        except Exception as e:
            print(f"⚠️  Aviso ao inicializar storage: {e}")
            # Não falha aqui, tenta novamente na próxima requisição

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Registrar handlers de erro ANTES das rotas para garantir que funcionem
@app.errorhandler(404)
def not_found(error):
    # Se for uma rota de API, retornar JSON
    if request.path.startswith('/api/'):
        return jsonify({'erro': 'Rota não encontrada'}), 404
    # Caso contrário, retornar HTML normal (para páginas)
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    # Se for uma rota de API, retornar JSON
    if request.path.startswith('/api/'):
        import traceback
        traceback.print_exc()
        return jsonify({'erro': 'Erro interno do servidor'}), 500
    # Caso contrário, retornar HTML normal
    return '<h1>Erro interno do servidor</h1>', 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Garante que todos os erros retornem JSON para rotas de API"""
    import traceback
    traceback.print_exc()
    # Se for uma rota de API, retornar JSON
    if request.path.startswith('/api/'):
        return jsonify({'erro': str(e)}), 500
    # Caso contrário, deixar o Flask tratar normalmente
    raise

@app.route('/')
def index():
    """Página principal"""
    # Não inicializar banco na página principal para evitar erros
    # O banco será inicializado quando necessário nas rotas de API
    return render_template('index.html')

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    """Lista todos os produtos"""
    ensure_db_initialized()
    conn = get_db()
    cursor = get_cursor(conn)
    cursor.execute('SELECT * FROM produtos ORDER BY data_atualizacao DESC')
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify([produto_para_dict(p) for p in produtos])

@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    """Cria um novo produto"""
    ensure_db_initialized()
    try:
        data = request.get_json()
        
        titulo = data.get('titulo', '').strip()
        if not titulo:
            return jsonify({'erro': 'Título é obrigatório'}), 400
        
        descricao = data.get('descricao', '').strip()
        quantidade = int(data.get('quantidade', 0))
        valor_compra = float(data.get('valor_compra', 0) or 0)
        imagem = data.get('imagem', '')
        especificacoes = data.get('especificacoes', '')
        
        # Converter especificações para JSON string se for dict
        if isinstance(especificacoes, dict):
            especificacoes = json.dumps(especificacoes, ensure_ascii=False)
        elif isinstance(especificacoes, str):
            try:
                # Validar se é JSON válido
                json.loads(especificacoes)
            except:
                especificacoes = json.dumps({}, ensure_ascii=False)
        else:
            especificacoes = json.dumps({}, ensure_ascii=False)
        
        ensure_db_initialized()
        if DATABASE_TYPE == 'postgresql':
            from datetime import datetime as dt
            data_atual = dt.now()
            conn = get_db()
            cursor = get_cursor(conn)
            cursor.execute('''
                INSERT INTO produtos (titulo, descricao, quantidade, valor_compra, imagem, especificacoes, data_criacao, data_atualizacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (titulo, descricao, quantidade, valor_compra, imagem, especificacoes, data_atual, data_atual))
            produto_id = cursor.fetchone()['id']
        else:
            data_atual = datetime.now().isoformat()
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO produtos (titulo, descricao, quantidade, valor_compra, imagem, especificacoes, data_criacao, data_atualizacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (titulo, descricao, quantidade, valor_compra, imagem, especificacoes, data_atual, data_atual))
            produto_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'id': produto_id, 'mensagem': 'Produto criado com sucesso'}), 201
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    """Obtém um produto específico"""
    ensure_db_initialized()
    conn = get_db()
    cursor = get_cursor(conn)
    placeholder = get_placeholder()
    cursor.execute(f'SELECT * FROM produtos WHERE id = {placeholder}', (produto_id,))
    produto = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if produto:
        return jsonify(produto_para_dict(produto))
    return jsonify({'erro': 'Produto não encontrado'}), 404

@app.route('/api/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    """Atualiza um produto existente"""
    ensure_db_initialized()
    try:
        data = request.get_json()
        
        conn = get_db()
        cursor = get_cursor(conn)
        placeholder = get_placeholder()
        
        # Verificar se o produto existe
        cursor.execute(f'SELECT * FROM produtos WHERE id = {placeholder}', (produto_id,))
        produto = cursor.fetchone()
        if not produto:
            cursor.close()
            conn.close()
            return jsonify({'erro': 'Produto não encontrado'}), 404
        
        # Atualizar campos
        titulo = data.get('titulo', produto['titulo']).strip()
        if not titulo:
            cursor.close()
            conn.close()
            return jsonify({'erro': 'Título é obrigatório'}), 400
        
        descricao = data.get('descricao', produto['descricao'])
        
        # Obter quantidade única
        if DATABASE_TYPE == 'postgresql':
            quantidade_existente = int(produto.get('quantidade', 0) or 0)
        else:
            try:
                quantidade_existente = int(produto['quantidade'] if produto['quantidade'] is not None else 0)
            except (KeyError, ValueError, TypeError):
                quantidade_existente = 0
        
        quantidade = int(data.get('quantidade', quantidade_existente))
        valor_compra_existente = float(produto.get('valor_compra', 0) or 0) if DATABASE_TYPE == 'postgresql' else float(produto.get('valor_compra', 0) or 0)
        valor_compra = float(data.get('valor_compra', valor_compra_existente) or 0)
        imagem_nova = data.get('imagem', produto['imagem'])
        imagem_antiga = produto['imagem']
        especificacoes = data.get('especificacoes', produto['especificacoes'])
        
        # Se a imagem mudou e havia uma imagem antiga, verificar se pode deletar
        if imagem_nova != imagem_antiga and imagem_antiga:
            # Verificar se a imagem antiga não é uma URL externa (Unsplash, etc)
            if not imagem_antiga.startswith('https://source.unsplash.com') and not imagem_antiga.startswith('http://source.unsplash.com'):
                # Verificar se a imagem está sendo usada por outro produto
                if DATABASE_TYPE == 'postgresql':
                    cursor.execute('SELECT COUNT(*) as total FROM produtos WHERE imagem = %s AND id != %s', (imagem_antiga, produto_id))
                else:
                    cursor.execute('SELECT COUNT(*) as total FROM produtos WHERE imagem = ? AND id != ?', (imagem_antiga, produto_id))
                resultado = cursor.fetchone()
                # Extrair o valor do COUNT de forma compatível
                if isinstance(resultado, dict):
                    total_uso = resultado.get('total', 0)
                elif isinstance(resultado, tuple):
                    total_uso = resultado[0] if len(resultado) > 0 else 0
                else:
                    total_uso = 0
                
                # Só deletar se nenhum outro produto estiver usando
                if total_uso == 0:
                    if STORAGE_CLOUD_DISPONIVEL and deletar_imagem_cloud:
                        # Deletar do Supabase Storage
                        try:
                            deletar_imagem_cloud(imagem_antiga)
                            print(f"✅ Imagem antiga deletada do storage: {imagem_antiga}")
                        except Exception as e:
                            print(f"⚠️  Erro ao deletar imagem antiga do storage: {e}")
                    else:
                        # Deletar do armazenamento local
                        try:
                            # Se for URL completa, extrair apenas o nome do arquivo
                            nome_arquivo = imagem_antiga
                            if imagem_antiga.startswith('http'):
                                nome_arquivo = imagem_antiga.split('/')[-1]
                            
                            imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
                            if os.path.exists(imagem_path):
                                os.remove(imagem_path)
                                print(f"✅ Imagem antiga deletada localmente: {nome_arquivo}")
                        except Exception as e:
                            print(f"⚠️  Erro ao deletar imagem antiga localmente: {e}")
                else:
                    print(f"ℹ️  Imagem antiga não deletada: está sendo usada por {total_uso} outro(s) produto(s)")
        
        imagem = imagem_nova
        
        # Converter especificações para JSON string se for dict
        if isinstance(especificacoes, dict):
            especificacoes = json.dumps(especificacoes, ensure_ascii=False)
        elif isinstance(especificacoes, str):
            try:
                json.loads(especificacoes)
            except:
                especificacoes = json.dumps({}, ensure_ascii=False)
        else:
            especificacoes = json.dumps({}, ensure_ascii=False)
        
        if DATABASE_TYPE == 'postgresql':
            from datetime import datetime as dt
            data_atual = dt.now()
            cursor.execute('''
                UPDATE produtos 
                SET titulo = %s, descricao = %s, quantidade = %s, valor_compra = %s, imagem = %s, especificacoes = %s, data_atualizacao = %s
                WHERE id = %s
            ''', (titulo, descricao, quantidade, valor_compra, imagem, especificacoes, data_atual, produto_id))
        else:
            data_atual = datetime.now().isoformat()
            cursor.execute('''
                UPDATE produtos 
                SET titulo = ?, descricao = ?, quantidade = ?, valor_compra = ?, imagem = ?, especificacoes = ?, data_atualizacao = ?
                WHERE id = ?
            ''', (titulo, descricao, quantidade, valor_compra, imagem, especificacoes, data_atual, produto_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'mensagem': 'Produto atualizado com sucesso'})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    """Deleta um produto"""
    ensure_db_initialized()
    try:
        conn = get_db()
        cursor = get_cursor(conn)
        placeholder = get_placeholder()
        
        # Verificar se o produto existe e obter imagem
        cursor.execute(f'SELECT imagem FROM produtos WHERE id = {placeholder}', (produto_id,))
        produto = cursor.fetchone()
        
        if not produto:
            cursor.close()
            conn.close()
            return jsonify({'erro': 'Produto não encontrado'}), 404
        
        # Antes de deletar, garantir que produto_titulo esteja salvo em todas as vendas
        # (caso ainda não esteja por algum motivo)
        if DATABASE_TYPE == 'postgresql':
            cursor.execute('''
                UPDATE vendas v
                SET produto_titulo = p.titulo
                FROM produtos p
                WHERE v.produto_id = p.id 
                AND v.produto_id = %s
                AND (v.produto_titulo IS NULL OR v.produto_titulo = '')
            ''', (produto_id,))
        else:
            cursor.execute('''
                UPDATE vendas 
                SET produto_titulo = (SELECT titulo FROM produtos WHERE produtos.id = vendas.produto_id)
                WHERE produto_id = ?
                AND (produto_titulo IS NULL OR produto_titulo = '')
            ''', (produto_id,))
        
        # Deletar imagem se existir e não estiver sendo usada por outro produto
        imagem_para_deletar = produto['imagem'] if DATABASE_TYPE == 'postgresql' else produto.get('imagem', '')
        if imagem_para_deletar:
            # Verificar se é uma URL externa (Unsplash, etc) - não precisa deletar
            if imagem_para_deletar.startswith('https://source.unsplash.com') or imagem_para_deletar.startswith('http://source.unsplash.com'):
                print(f"ℹ️  Imagem é URL externa (Unsplash), não será deletada: {imagem_para_deletar}")
            else:
                # Verificar se a imagem está sendo usada por outro produto
                if DATABASE_TYPE == 'postgresql':
                    cursor.execute('SELECT COUNT(*) as total FROM produtos WHERE imagem = %s AND id != %s', (imagem_para_deletar, produto_id))
                else:
                    cursor.execute('SELECT COUNT(*) as total FROM produtos WHERE imagem = ? AND id != ?', (imagem_para_deletar, produto_id))
                resultado = cursor.fetchone()
                # Extrair o valor do COUNT de forma compatível
                if isinstance(resultado, dict):
                    total_uso = resultado.get('total', 0)
                elif isinstance(resultado, tuple):
                    total_uso = resultado[0] if len(resultado) > 0 else 0
                else:
                    total_uso = 0
                
                # Só deletar se nenhum outro produto estiver usando
                if total_uso == 0:
                    if STORAGE_CLOUD_DISPONIVEL and deletar_imagem_cloud:
                        # Deletar do Supabase Storage
                        try:
                            deletar_imagem_cloud(imagem_para_deletar)
                            print(f"✅ Imagem deletada do Supabase Storage: {imagem_para_deletar}")
                        except Exception as e:
                            print(f"⚠️  Erro ao deletar imagem do Supabase Storage: {e}")
                    else:
                        # Deletar do armazenamento local
                        try:
                            # Se for URL completa, extrair apenas o nome do arquivo
                            nome_arquivo = imagem_para_deletar
                            if imagem_para_deletar.startswith('http'):
                                nome_arquivo = imagem_para_deletar.split('/')[-1]
                            
                            imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
                            if os.path.exists(imagem_path):
                                os.remove(imagem_path)
                                print(f"✅ Imagem deletada localmente: {nome_arquivo}")
                        except Exception as e:
                            print(f"⚠️  Erro ao deletar imagem localmente: {e}")
                else:
                    print(f"ℹ️  Imagem não deletada: está sendo usada por {total_uso} outro(s) produto(s)")
        
        # Deletar produto
        cursor.execute(f'DELETE FROM produtos WHERE id = {placeholder}', (produto_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'mensagem': 'Produto deletado com sucesso'})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_imagem():
    """Faz upload de uma imagem"""
    if 'imagem' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['imagem']
    if file.filename == '':
        return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Adicionar timestamp para evitar conflitos
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        # Tentar usar Supabase Storage se configurado
        ensure_storage_initialized()
        if STORAGE_CLOUD_DISPONIVEL and upload_imagem_cloud:
            try:
                url_imagem = upload_imagem_cloud(file, filename)
                return jsonify({
                    'imagem': url_imagem,  # Retorna URL completa da imagem
                    'mensagem': 'Imagem enviada com sucesso para Supabase Storage'
                })
            except Exception as e:
                return jsonify({'erro': f'Erro ao fazer upload para nuvem: {str(e)}'}), 500
        else:
            # Fallback: armazenamento local
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return jsonify({
                'imagem': filename,  # Retorna apenas o nome do arquivo
                'mensagem': 'Imagem enviada com sucesso (armazenamento local)'
            })
    
    return jsonify({'erro': 'Tipo de arquivo não permitido'}), 400

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """Serve arquivos de upload (apenas para armazenamento local)"""
    # Se for uma URL completa (Supabase), redirecionar
    if filename.startswith('http'):
        from flask import redirect
        return redirect(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/vendas', methods=['GET'])
def listar_vendas():
    """Lista todas as vendas ordenadas por data (mais recente primeiro)"""
    ensure_db_initialized()
    conn = get_db()
    cursor = get_cursor(conn)
    
    # Buscar vendas (usar produto_titulo da tabela vendas se produto foi deletado)
    if DATABASE_TYPE == 'postgresql':
        cursor.execute('''
            SELECT v.*, 
                   COALESCE(v.produto_titulo, p.titulo, 'Produto Deletado') as produto_titulo_final
            FROM vendas v
            LEFT JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC, v.data_criacao DESC
        ''')
    else:
        cursor.execute('''
            SELECT v.*, 
                   COALESCE(v.produto_titulo, p.titulo, 'Produto Deletado') as produto_titulo_final
            FROM vendas v
            LEFT JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC, v.data_criacao DESC
        ''')
    
    vendas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Converter para dict com informações do produto
    vendas_dict = []
    for venda in vendas:
        if DATABASE_TYPE == 'postgresql':
            produto_titulo = venda.get('produto_titulo_final', venda.get('produto_titulo', 'Produto Deletado'))
        else:
            produto_titulo = venda.get('produto_titulo_final', venda.get('produto_titulo', 'Produto Deletado'))
        vendas_dict.append(venda_para_dict(venda, produto_titulo))
    
    return jsonify(vendas_dict)

@app.route('/api/vendas', methods=['POST'])
def criar_venda():
    """Cria uma nova venda e diminui o estoque do produto"""
    ensure_db_initialized()
    try:
        data = request.get_json()
        
        produto_id = int(data.get('produto_id', 0))
        valor_venda = float(data.get('valor_venda', 0) or 0)
        data_venda = data.get('data_venda', '').strip()
        onde_vendeu = data.get('onde_vendeu', '').strip()
        observacoes = data.get('observacoes', '').strip()
        
        # Validações
        if produto_id <= 0:
            return jsonify({'erro': 'Produto é obrigatório'}), 400
        
        if valor_venda <= 0:
            return jsonify({'erro': 'Valor de venda deve ser maior que zero'}), 400
        
        if not data_venda:
            return jsonify({'erro': 'Data da venda é obrigatória'}), 400
        
        if onde_vendeu not in ['mercado_livre', 'shopee']:
            return jsonify({'erro': 'Onde vendeu deve ser "mercado_livre" ou "shopee"'}), 400
        
        conn = get_db()
        cursor = get_cursor(conn)
        placeholder = get_placeholder()
        
        # Buscar produto para obter valor_compra e verificar estoque
        cursor.execute(f'SELECT * FROM produtos WHERE id = {placeholder}', (produto_id,))
        produto = cursor.fetchone()
        
        if not produto:
            cursor.close()
            conn.close()
            return jsonify({'erro': 'Produto não encontrado'}), 404
        
        # Obter valor de compra, quantidade e título do produto
        if DATABASE_TYPE == 'postgresql':
            valor_compra = float(produto.get('valor_compra', 0) or 0)
            quantidade = int(produto.get('quantidade', 0) or 0)
            produto_titulo = produto.get('titulo', '')
        else:
            valor_compra = float(produto['valor_compra'] if produto['valor_compra'] is not None else 0)
            try:
                quantidade = int(produto['quantidade'] if produto['quantidade'] is not None else 0)
            except (KeyError, ValueError, TypeError):
                quantidade = 0
            produto_titulo = produto.get('titulo', '') or ''
        
        # Verificar se há estoque disponível
        if quantidade <= 0:
            cursor.close()
            conn.close()
            return jsonify({'erro': 'Estoque insuficiente'}), 400
        
        # Diminuir estoque
        nova_quantidade = quantidade - 1
        if DATABASE_TYPE == 'postgresql':
            from datetime import datetime as dt
            data_atual = dt.now()
            cursor.execute('''
                UPDATE produtos 
                SET quantidade = %s, data_atualizacao = %s
                WHERE id = %s
            ''', (nova_quantidade, data_atual, produto_id))
        else:
            data_atual = datetime.now().isoformat()
            cursor.execute('''
                UPDATE produtos 
                SET quantidade = ?, data_atualizacao = ?
                WHERE id = ?
            ''', (nova_quantidade, data_atual, produto_id))
        
        # Criar venda (salvar produto_titulo para preservar mesmo se produto for deletado)
        if DATABASE_TYPE == 'postgresql':
            from datetime import datetime as dt
            data_criacao = dt.now()
            cursor.execute('''
                INSERT INTO vendas (produto_id, produto_titulo, valor_venda, valor_compra, data_venda, onde_vendeu, observacoes, data_criacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (produto_id, produto_titulo, valor_venda, valor_compra, data_venda, onde_vendeu, observacoes, data_criacao))
            venda_id = cursor.fetchone()['id']
        else:
            data_criacao = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO vendas (produto_id, produto_titulo, valor_venda, valor_compra, data_venda, onde_vendeu, observacoes, data_criacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (produto_id, produto_titulo, valor_venda, valor_compra, data_venda, onde_vendeu, observacoes, data_criacao))
            venda_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'id': venda_id, 'mensagem': 'Venda registrada com sucesso'}), 201
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500

# Handlers de erro já registrados acima (antes das rotas)

# Para desenvolvimento local e produção
if __name__ == '__main__':
    # Porta do ambiente (Railway, Render, etc) ou padrão 5001
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
