# ✅ Solução: Session Pooler para Vercel (IPv4-compatible)

## 🎯 Problema Resolvido!

O **Session Pooler** do Supabase é **IPv4 proxied for free** e funciona perfeitamente com Vercel!

## 📋 Connection String do Session Pooler

A connection string do Session Pooler é diferente da Direct Connection:

```
postgresql://postgres.htrghiefnoaytjmcdbuk:[YOUR-PASSWORD]@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

**Diferenças importantes:**
- ✅ **Host:** `aws-0-us-west-2.pooler.supabase.com` (não `db.xxxxx.supabase.co`)
- ✅ **Porta:** `5432` (não 6543!)
- ✅ **User:** `postgres.htrghiefnoaytjmcdbuk` (formato: `postgres.PROJECT_REF`)
- ✅ **IPv4 proxied:** Funciona com Vercel (IPv4-only)

## 🚀 Configuração no Vercel

### Opção 1: Usar DATABASE_URL (Recomendado - Mais Simples)

No **Vercel Dashboard** → **Settings** → **Environment Variables**, adicione:

```
DATABASE_URL=postgresql://postgres.htrghiefnoaytjmcdbuk:S%26mur%26i77681271@aws-0-us-west-2.pooler.supabase.com:5432/postgres
DB_PASSWORD=S&mur&i77681271
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**Importante:** 
- Substitua `S%26mur%26i77681271` pela sua senha com URL encoding (`&` vira `%26`)
- Ou copie a connection string completa do Supabase Dashboard (já vem com encoding correto)

### Opção 2: Variáveis Individuais

Se preferir usar variáveis individuais:

```
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.htrghiefnoaytjmcdbuk
DB_PASSWORD=S&mur&i77681271
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**Diferenças:**
- `DB_HOST` = `aws-0-us-west-2.pooler.supabase.com` (Session Pooler)
- `DB_USER` = `postgres.htrghiefnoaytjmcdbuk` (com PROJECT_REF)

## 🔍 Como Obter a Connection String Correta

1. **Acesse:** https://supabase.com/dashboard
2. **Selecione seu projeto**
3. **Vá em:** Settings → Database
4. **Role até:** Connection Pooling
5. **Procure por:** "Session Pooler" (não Direct Connection)
6. **Copie a Connection String** completa
7. **Substitua** `[YOUR-PASSWORD]` pela sua senha

## ✅ Por Que Session Pooler Funciona

- ✅ **IPv4 proxied for free** - Compatível com Vercel (IPv4-only)
- ✅ **Mesma porta 5432** - Mas através do pooler (proxy IPv4)
- ✅ **User especial** - Formato `postgres.PROJECT_REF` para identificar o projeto
- ✅ **Gratuito** - Não precisa comprar IPv4 add-on

## 🚀 Próximos Passos

1. **Copie a Connection String do Session Pooler** do Supabase Dashboard
2. **Adicione no Vercel como `DATABASE_URL`** (ou use variáveis individuais)
3. **Faça redeploy**
4. **Teste:** `https://seu-projeto.vercel.app/api/debug/banco`

## 💡 Nota

O código já está preparado para usar essas configurações. Basta copiar a connection string correta do Supabase Dashboard e configurar no Vercel.

