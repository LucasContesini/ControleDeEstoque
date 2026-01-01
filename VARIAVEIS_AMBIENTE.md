# Variáveis de Ambiente - Controle de Estoque

## 📋 Lista Completa de Variáveis

### ✅ OBRIGATÓRIAS para Produção (Vercel)

#### 1. Supabase Storage
```
SUPABASE_URL=https://htrghiefnoaytjmcdbuk.supabase.co
SUPABASE_KEY=[Chave anon/public - JWT que começa com eyJ...]
SUPABASE_SERVICE_KEY=[Chave service_role - JWT que começa com eyJ...]
```

**⚠️ IMPORTANTE:** 
- A API REST do Supabase Storage requer chaves JWT tradicionais (que começam com `eyJ...`)
- As novas chaves `sb_publishable_` e `sb_secret_` NÃO funcionam com a API REST de Storage
- Obtenha as chaves JWT em: **Supabase Dashboard → Settings → API → anon key** e **service_role key**

#### 2. Banco de Dados PostgreSQL
```
DATABASE_URL=postgresql://postgres.htrghiefnoaytjmcdbuk:SENHA@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

**OU** (se não usar DATABASE_URL):
```
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.htrghiefnoaytjmcdbuk
DB_PASSWORD=SENHA
```

### 🔧 OPCIONAIS

```
BUCKET_NAME=Controle de Estoque
```
(Nome do bucket no Supabase Storage - padrão: "Controle de Estoque")

## 📍 Onde Obter as Chaves

### Supabase Dashboard
1. Acesse: https://supabase.com/dashboard/project/htrghiefnoaytjmcdbuk/settings/api
2. **anon/public key**: Copie a chave "anon" ou "public" (JWT que começa com `eyJ...`)
3. **service_role key**: Copie a chave "service_role" (JWT que começa com `eyJ...`)
   - ⚠️ Esta chave é SECRETA - nunca exponha no frontend!

### Database Connection String
1. Acesse: https://supabase.com/dashboard/project/htrghiefnoaytjmcdbuk/settings/database
2. Vá em **Connection Pooling** → **Session Pooler**
3. Copie a **Connection String** (não use Direct Connection no Vercel!)

## 🔍 Verificação

### Variáveis Necessárias no Vercel:
- ✅ `SUPABASE_URL`
- ✅ `SUPABASE_KEY` (JWT anon key - começa com `eyJ...`)
- ✅ `SUPABASE_SERVICE_KEY` (JWT service_role key - começa com `eyJ...`)
- ✅ `DATABASE_URL` (ou variáveis DB_ individuais)

### Formato das Chaves:
- ✅ **Correto**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (JWT)
- ❌ **Incorreto**: `sb_publishable_...` ou `sb_secret_...` (não funciona com API REST de Storage)

## 🚨 Problemas Comuns

### "Invalid API key" ou "Invalid Compact JWS"
- **Causa**: Usando chaves `sb_*` em vez de chaves JWT `eyJ...`
- **Solução**: Use as chaves JWT tradicionais do Supabase Dashboard

### "Supabase Storage não configurado"
- **Causa**: Variáveis de ambiente não configuradas no Vercel
- **Solução**: Adicione todas as variáveis obrigatórias no Vercel Dashboard

### "Cannot assign requested address" (banco de dados)
- **Causa**: Usando Direct Connection em vez de Session Pooler
- **Solução**: Use a connection string do Session Pooler

