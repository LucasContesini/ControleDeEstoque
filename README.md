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

### 2. Configurar Variáveis de Ambiente (Opcional para desenvolvimento)

Para desenvolvimento local com SQLite, não precisa configurar nada. O sistema detecta automaticamente.

Para usar PostgreSQL/Supabase localmente:

```bash
cp env.example .env
# Edite o .env com suas credenciais
```

### 3. Iniciar Aplicação

**Opção A: Script Automático (Recomendado)**
```bash
./iniciar.sh
```

**Opção B: Manual**
```bash
python3 app.py
```

### 4. Acessar

Abra no navegador: **http://localhost:5001**

**Nota:** A porta 5001 é usada porque a porta 5000 padrão está ocupada pelo AirPlay Receiver no macOS.

## Deploy no Vercel

### ⚠️ Importante: Vercel é IPv4-only!

O Vercel não suporta IPv6. Use o **Session Pooler** do Supabase (não a Direct Connection).

### Configuração

1. **No Supabase Dashboard:**
   - Vá em **Settings** → **Database** → **Connection Pooling**
   - Copie a **Connection String** do **Session Pooler** (não Direct Connection)

2. **No Vercel Dashboard:**
   - Vá em **Settings** → **Environment Variables**
   - Adicione as seguintes variáveis:

```
DATABASE_URL=[Connection String do Session Pooler do Supabase]
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_anon_key
SUPABASE_SERVICE_KEY=sua_service_key
```

**Ou use variáveis individuais:**

```
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.PROJECT_REF
DB_PASSWORD=sua_senha
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_anon_key
SUPABASE_SERVICE_KEY=sua_service_key
```

### Variáveis Necessárias

| Variável | Descrição | Onde Obter |
|---------|-----------|------------|
| `DATABASE_URL` ou `DB_HOST/DB_PORT/DB_USER/DB_PASSWORD` | Connection string ou credenciais do Session Pooler | Supabase Dashboard → Database → Connection Pooling |
| `SUPABASE_URL` | URL do projeto Supabase | Supabase Dashboard → Settings → API |
| `SUPABASE_KEY` | Chave pública (anon key) | Supabase Dashboard → Settings → API |
| `SUPABASE_SERVICE_KEY` | Chave secreta (service_role) | Supabase Dashboard → Settings → API |

## Estrutura do Projeto

```
controle-de-estoque/
├── app.py                  # Aplicação Flask principal
├── models.py               # Modelo de dados
├── config.py               # Configurações centralizadas
├── db_helper.py            # Helper de banco de dados
├── storage.py              # Storage Supabase (API REST)
├── storage_s3.py            # Storage Supabase (S3 - fallback)
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
- Verifique se está usando **Session Pooler** (não Direct Connection)
- Verifique se as variáveis de ambiente estão configuradas corretamente
- Verifique se o bucket "Controle de Estoque" existe e está público no Supabase

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
- Se `DATABASE_TYPE=postgresql` ou estiver no Vercel → usa PostgreSQL/Supabase
- Caso contrário → usa SQLite local

### Storage

O sistema tenta usar Supabase Storage na seguinte ordem:
1. API REST do Supabase (via `storage.py`)
2. S3 API do Supabase (via `storage_s3.py`)
3. Armazenamento local (`static/uploads/`)

## Licença

Projeto pessoal para controle de estoque.
