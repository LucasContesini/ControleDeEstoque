# Controle de Estoque

Sistema simples de controle de estoque para produtos vendidos no Mercado Livre e Shopee.

## Funcionalidades

- ✅ Inserir produtos
- ✅ Alterar produtos
- ✅ Remover produtos
- ✅ Gerenciar quantidade em estoque por e-commerce (Mercado Livre e Shopee)
- ✅ Upload de imagens (armazenamento em nuvem)
- ✅ Campos: título, descrição, especificações adicionais
- ✅ Ordenação por nome, quantidade e data de modificação
- ✅ Busca de produtos
- ✅ Interface responsiva (desktop, tablet e mobile)

## Tecnologias

- **Backend:** Python + Flask
- **Frontend:** HTML, CSS, JavaScript
- **Banco de Dados:** SQLite (desenvolvimento) ou PostgreSQL/Supabase (produção)
- **Storage:** Supabase Storage (imagens na nuvem)

## Instalação Rápida

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar Aplicação

**Opção A: Script Automático (Recomendado)**
```bash
./iniciar.sh
```

**Opção B: Manual**
```bash
python3 app.py
```

### 3. Acessar

Abra no navegador: **http://localhost:5001**

**Nota:** A porta 5001 é usada porque a porta 5000 padrão está ocupada pelo AirPlay Receiver no macOS.

## Configuração para Produção (Supabase)

### 1. Configurar Banco de Dados

Edite o arquivo `configurar_supabase.sh` e configure:

```bash
export DATABASE_TYPE=postgresql
export DB_HOST=db.xxxxx.supabase.co
export DB_PORT=5432
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASSWORD=sua_senha
```

**Como obter as credenciais:**
1. Acesse https://supabase.com
2. Selecione seu projeto → **Settings** → **Database**
3. Copie a string de conexão e extraia as informações

### 2. Configurar Storage (Imagens)

No mesmo arquivo `configurar_supabase.sh`, adicione:

```bash
export SUPABASE_URL="https://xxxxx.supabase.co"
export SUPABASE_KEY="sua_anon_key"
export SUPABASE_SERVICE_KEY="sua_service_key"
```

**Como obter as chaves:**
1. No Supabase, vá em **Settings** → **API**
2. Copie a chave **anon public** (para `SUPABASE_KEY`)
3. Copie a chave **service_role** (para `SUPABASE_SERVICE_KEY`)

### 3. Criar Bucket no Supabase Storage

1. No Supabase, vá em **Storage**
2. Clique em **New bucket**
3. Nome: `Controle de Estoque`
4. Marque **Public bucket**
5. Clique em **Create bucket**

### 4. Iniciar

```bash
./iniciar.sh
```

## Estrutura do Projeto

```
controle-de-estoque/
├── app.py                  # Aplicação Flask principal
├── models.py               # Modelo de dados
├── db_helper.py            # Helper de banco de dados
├── storage.py              # Storage Supabase (API REST)
├── storage_s3.py            # Storage Supabase (S3 - fallback)
├── configurar_supabase.sh  # Script de configuração
├── iniciar.sh              # Script de inicialização
├── requirements.txt        # Dependências Python
├── static/                 # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── uploads/           # Uploads locais (fallback)
├── templates/             # Templates HTML
└── database.db            # Banco SQLite (criado automaticamente)
```

## Funcionalidades Detalhadas

### Quantidade por E-commerce

- Cada produto tem quantidade separada para Mercado Livre e Shopee
- A quantidade total é calculada automaticamente (ML + Shopee)
- Exibição visual com badges coloridos

### Upload de Imagens

- **Produção:** Imagens são salvas no Supabase Storage (acessíveis de qualquer dispositivo)
- **Desenvolvimento:** Imagens são salvas localmente em `static/uploads/`
- Placeholder automático quando não há imagem

### Ordenação

- Por nome (A-Z ou Z-A)
- Por quantidade (maior ou menor)
- Por data de modificação (mais recente primeiro)

## Troubleshooting

### Porta 5001 já em uso
```bash
pkill -f "python3 app.py"
./iniciar.sh
```

### Erro de conexão com Supabase
- Verifique se a senha está correta em `configurar_supabase.sh`
- Verifique se o bucket "Controle de Estoque" existe e está público
- Verifique os logs do servidor

### Dependências faltando
```bash
pip3 install -r requirements.txt
```

### Imagens não aparecem
- Verifique se o bucket está marcado como **Public** no Supabase
- Verifique se as chaves (`SUPABASE_KEY` e `SUPABASE_SERVICE_KEY`) estão corretas
- Verifique as URLs no console do navegador (F12)

## Desenvolvimento

### Banco de Dados

O sistema detecta automaticamente qual banco usar:
- Se `DATABASE_TYPE=postgresql` → usa PostgreSQL/Supabase
- Caso contrário → usa SQLite local

### Storage

O sistema tenta usar Supabase Storage na seguinte ordem:
1. API REST do Supabase (via `storage.py`)
2. S3 API do Supabase (via `storage_s3.py`)
3. Armazenamento local (`static/uploads/`)

## Licença

Projeto pessoal para controle de estoque.
