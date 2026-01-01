# Variáveis de Ambiente - Controle de Estoque

Este documento lista todas as variáveis de ambiente necessárias para configurar o sistema em um provedor de hospedagem.

## 📋 Variáveis Obrigatórias

### 🗄️ Banco de Dados (PostgreSQL/Supabase)

| Variável | Descrição | Exemplo | Obrigatória |
|---------|-----------|---------|-------------|
| `DATABASE_TYPE` | Tipo de banco: `sqlite` (dev) ou `postgresql` (prod) | `postgresql` | ✅ Sim |
| `DB_HOST` | Host do banco de dados | `db.xxxxx.supabase.co` | ✅ Sim (se PostgreSQL) |
| `DB_PORT` | Porta do banco de dados | `5432` | ✅ Sim (se PostgreSQL) |
| `DB_NAME` | Nome do banco de dados | `postgres` | ✅ Sim (se PostgreSQL) |
| `DB_USER` | Usuário do banco de dados | `postgres` | ✅ Sim (se PostgreSQL) |
| `DB_PASSWORD` | Senha do banco de dados | `sua_senha_aqui` | ✅ Sim (se PostgreSQL) |

**Nota:** Se usar SQLite (desenvolvimento), apenas `DATABASE_TYPE=sqlite` é necessário. O arquivo será criado automaticamente.

---

### 📦 Storage de Imagens (Supabase Storage)

#### Opção 1: API REST (Recomendado)

| Variável | Descrição | Onde Obter | Obrigatória |
|---------|-----------|------------|-------------|
| `SUPABASE_URL` | URL do projeto Supabase | Settings → API → Project URL | ✅ Sim |
| `SUPABASE_KEY` | Chave pública (anon key) | Settings → API → anon public key | ✅ Sim |
| `SUPABASE_SERVICE_KEY` | Chave de serviço (service_role) | Settings → API → service_role key | ✅ Sim |

**Como obter:**
1. Acesse seu projeto no Supabase
2. Vá em **Settings** → **API**
3. Copie:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** → `SUPABASE_KEY`
   - **service_role** → `SUPABASE_SERVICE_KEY` ⚠️ **MANTENHA SECRETO!**

#### Opção 2: S3 API (Alternativa)

| Variável | Descrição | Onde Obter | Obrigatória |
|---------|-----------|------------|-------------|
| `SUPABASE_S3_ENDPOINT` | Endpoint S3 do Supabase | Settings → Storage → S3 Settings | ⚠️ Opcional |
| `SUPABASE_S3_ACCESS_KEY` | Access Key S3 | Settings → Storage → S3 Settings | ⚠️ Opcional |
| `SUPABASE_S3_SECRET_KEY` | Secret Key S3 | Settings → Storage → S3 Settings | ⚠️ Opcional |
| `SUPABASE_S3_REGION` | Região S3 | Geralmente `us-west-2` | ⚠️ Opcional |

**Nota:** Use apenas se preferir S3 ao invés da API REST. A API REST é recomendada por ser mais simples.

---

## 🔧 Configuração por Provedor

### Heroku

```bash
heroku config:set DATABASE_TYPE=postgresql
heroku config:set DB_HOST=db.xxxxx.supabase.co
heroku config:set DB_PORT=5432
heroku config:set DB_NAME=postgres
heroku config:set DB_USER=postgres
heroku config:set DB_PASSWORD=sua_senha
heroku config:set SUPABASE_URL=https://xxxxx.supabase.co
heroku config:set SUPABASE_KEY=sua_anon_key
heroku config:set SUPABASE_SERVICE_KEY=sua_service_key
```

### Vercel

No dashboard do Vercel, vá em **Settings** → **Environment Variables** e adicione todas as variáveis acima.

⚠️ **Importante:** Adicione as variáveis para todos os ambientes (Production, Preview, Development).

---

## 📝 Arquivo .env (Desenvolvimento Local)

Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de Dados
DATABASE_TYPE=postgresql
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui

# Supabase Storage (API REST - Recomendado)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=sua_anon_key
SUPABASE_SERVICE_KEY=sua_service_key

# Supabase Storage (S3 - Opcional)
# SUPABASE_S3_ENDPOINT=https://xxxxx.storage.supabase.co
# SUPABASE_S3_ACCESS_KEY=sua_access_key
# SUPABASE_S3_SECRET_KEY=sua_secret_key
# SUPABASE_S3_REGION=us-west-2
```

**Importante:** Adicione `.env` ao `.gitignore` para não commitar credenciais!

---

## ✅ Checklist de Configuração

Antes de fazer deploy, certifique-se de:

- [ ] Todas as variáveis de banco de dados estão configuradas
- [ ] `SUPABASE_URL`, `SUPABASE_KEY` e `SUPABASE_SERVICE_KEY` estão configuradas
- [ ] O bucket "Controle de Estoque" foi criado no Supabase Storage
- [ ] As políticas de Row Level Security (RLS) estão configuradas no Supabase (se necessário)
- [ ] O arquivo `.env` está no `.gitignore`
- [ ] As credenciais não estão hardcoded no código

---

## 🔒 Segurança

⚠️ **IMPORTANTE:**

1. **NUNCA** commite credenciais no Git
2. **NUNCA** compartilhe `SUPABASE_SERVICE_KEY` publicamente
3. Use variáveis de ambiente sempre
4. Revise as políticas de RLS no Supabase
5. Use HTTPS em produção

---

## 🧪 Testar Configuração

Após configurar as variáveis, teste a conexão:

```bash
# Testar banco de dados
python3 -c "from models import init_db; init_db(); print('✅ Banco OK')"

# Testar storage (se configurado)
python3 -c "from storage import usar_storage_cloud; print('✅ Storage OK' if usar_storage_cloud() else '❌ Storage não configurado')"
```

---

## 📚 Referências

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Storage Guide](https://supabase.com/docs/guides/storage)
- [PostgreSQL Connection Strings](https://www.postgresql.org/docs/current/libpq-connect.html)

