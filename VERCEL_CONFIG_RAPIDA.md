# ⚡ Configuração Rápida - Vercel + Supabase

## 🎯 Solução para o Erro "Cannot assign requested address"

O código agora **detecta automaticamente** que está no Vercel e usa **Connection Pooling** (porta 6543) por padrão.

## ✅ Configuração no Vercel

### Opção 1: Variáveis Individuais (Recomendado)

No **Vercel Dashboard** → **Settings** → **Environment Variables**, adicione:

```
DATABASE_TYPE=postgresql
DB_HOST=db.htrghiefnoaytjmcdbuk.supabase.co
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=S&mur&i77681271
SUPABASE_URL=https://htrghiefnoaytjmcdbuk.supabase.co
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**⚠️ IMPORTANTE:** 
- `DB_PORT=6543` (porta de pooling, não 5432!)
- Não precisa definir `USE_CONNECTION_POOLING` - o código detecta automaticamente que está no Vercel

### Opção 2: DATABASE_URL com Pooling

Se preferir usar connection string:

```
DATABASE_URL=postgresql://postgres:S%26mur%26i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:6543/postgres?sslmode=require
DATABASE_TYPE=postgresql
SUPABASE_URL=https://htrghiefnoaytjmcdbuk.supabase.co
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**⚠️ IMPORTANTE:**
- Porta na URL deve ser **:6543** (pooling), não :5432
- Se a senha contém `&`, use URL encoding: `%26` (exemplo acima)

## 🔍 Verificar Configuração

Após fazer deploy, acesse:

```
https://seu-projeto.vercel.app/api/debug/banco
```

Isso mostrará:
- Se está detectando o Vercel corretamente
- Qual porta está sendo usada
- Se a conexão está funcionando

## 📋 Checklist

- [ ] Variáveis configuradas no Vercel
- [ ] `DB_PORT=6543` (ou porta 6543 na DATABASE_URL)
- [ ] Variáveis configuradas para **todos os ambientes** (Production, Preview, Development)
- [ ] Redeploy feito após configurar variáveis
- [ ] Testado em `/api/debug/banco`

## 🚀 O Que Mudou

O código agora:
- ✅ **Detecta automaticamente** se está no Vercel
- ✅ **Usa pooling (6543) por padrão** no Vercel
- ✅ **Substitui automaticamente** porta 5432 por 6543 se detectar pooling
- ✅ **Mostra informações de debug** na rota `/api/debug/banco`

## 💡 Por Que Pooling Funciona?

- ✅ Mais confiável em ambientes serverless
- ✅ Melhor gerenciamento de conexões
- ✅ Evita problemas com IPv6/IPv4
- ✅ Otimizado para Vercel

## 🆘 Ainda com Problemas?

1. **Verifique os logs do Vercel:**
   - Dashboard → Deployments → Functions → api/index.py

2. **Confirme a porta:**
   - Acesse `/api/debug/banco` e veja qual porta está sendo usada

3. **Teste localmente:**
   ```bash
   psql "postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:6543/postgres?sslmode=require"
   ```

