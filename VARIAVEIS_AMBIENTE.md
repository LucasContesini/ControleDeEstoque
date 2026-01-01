# Variáveis de Ambiente - Controle de Estoque

## ✅ Simplificado: Apenas 3 Variáveis Necessárias!

A maioria das configurações está hardcoded no arquivo `config.py`. Você só precisa configurar as **credenciais sensíveis**.

O sistema usa a **API REST do Supabase** por padrão (mais simples). As variáveis S3 são **opcionais** e só necessárias se a API REST não funcionar.

## 📋 Variáveis Obrigatórias (Apenas 3!)

| Variável | Descrição | Onde Obter | Obrigatória |
|---------|-----------|------------|-------------|
| `DB_PASSWORD` | Senha do banco de dados PostgreSQL | Supabase Dashboard → Settings → Database → Database password | ✅ Sim |
| `SUPABASE_KEY` | Chave pública (anon key) - para API REST | Supabase Dashboard → Settings → API → anon public key | ✅ Sim |
| `SUPABASE_SERVICE_KEY` | Chave de serviço (service_role) - para upload | Supabase Dashboard → Settings → API → service_role key | ✅ Sim |

## ⚠️ Variáveis S3 (Opcionais - Apenas se API REST não funcionar)

O sistema tenta usar a API REST primeiro. Só usa S3 como fallback se a API REST falhar.

| Variável | Descrição | Obrigatória |
|---------|-----------|-------------|
| `SUPABASE_S3_ENDPOINT` | Endpoint S3 do Supabase | ❌ Não (fallback) |
| `SUPABASE_S3_ACCESS_KEY` | Access Key S3 | ❌ Não (fallback) |
| `SUPABASE_S3_SECRET_KEY` | Secret Key S3 | ❌ Não (fallback) |
| `SUPABASE_S3_REGION` | Região S3 | ❌ Não (fallback) |

## 🔧 Configurações Hardcoded (Não Precisa Configurar)

As seguintes configurações estão no arquivo `config.py` e **não precisam** ser configuradas:

- ✅ `DB_HOST` - `db.htrghiefnoaytjmcdbuk.supabase.co`
- ✅ `DB_PORT` - `6543` (connection pooling)
- ✅ `DB_NAME` - `postgres`
- ✅ `DB_USER` - `postgres`
- ✅ `SUPABASE_URL` - `https://htrghiefnoaytjmcdbuk.supabase.co`
- ✅ `BUCKET_NAME` - `Controle de Estoque`
- ✅ `DATABASE_TYPE` - Detectado automaticamente (postgresql no Vercel, sqlite local)

## 📝 Como Obter as Credenciais

### 1. DB_PASSWORD (Senha do Banco)

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em **Settings** → **Database**
4. Role até **Database password**
5. Se não souber a senha, clique em **Reset database password**
6. Copie a senha gerada

### 2. SUPABASE_KEY (Chave Pública)

1. No Supabase Dashboard, vá em **Settings** → **API**
2. Em **Project API keys**, copie a chave **anon public**
3. Esta é a chave pública (pode ser exposta no frontend)

### 3. SUPABASE_SERVICE_KEY (Chave Secreta)

1. No mesmo lugar (Settings → API)
2. Copie a chave **service_role**
3. ⚠️ **MANTENHA SECRETO!** Esta chave tem permissões administrativas

## 🚀 Configuração no Vercel

No **Vercel Dashboard** → **Settings** → **Environment Variables**, adicione apenas:

```
DB_PASSWORD=S&mur&i77681271
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**Importante:** 
- Configure para **todos os ambientes** (Production, Preview, Development)
- Não precisa configurar as outras variáveis (estão hardcoded)

## 🔄 Opcional: DATABASE_URL

Se preferir usar uma connection string completa em vez de variáveis individuais, você pode adicionar:

```
DATABASE_URL=postgresql://postgres:S%26mur%26i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:6543/postgres?sslmode=require
```

**Nota:** Se usar `DATABASE_URL`, ainda precisa de `SUPABASE_KEY` e `SUPABASE_SERVICE_KEY` para o Storage.

## 📋 Checklist de Configuração

- [ ] `DB_PASSWORD` configurada no Vercel
- [ ] `SUPABASE_KEY` configurada no Vercel
- [ ] `SUPABASE_SERVICE_KEY` configurada no Vercel
- [ ] Variáveis configuradas para todos os ambientes (Production, Preview, Development)
- [ ] Bucket "Controle de Estoque" criado no Supabase Storage (público)

## 🔍 Verificar Configuração

Após configurar, acesse:

```
https://seu-projeto.vercel.app/api/debug/banco
```

Isso mostrará se a conexão está funcionando corretamente.

## 💡 Desenvolvimento Local

Para desenvolvimento local (SQLite), não precisa configurar nenhuma variável. O sistema detecta automaticamente e usa SQLite.

Para usar PostgreSQL localmente, adicione no seu `.env` ou `configurar_supabase.sh`:

```bash
export DB_PASSWORD=sua_senha
export SUPABASE_KEY=sua_anon_key
export SUPABASE_SERVICE_KEY=sua_service_key
```

Ou defina `DATABASE_TYPE=postgresql` para forçar PostgreSQL mesmo localmente.
