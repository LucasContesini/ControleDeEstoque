# 🔧 Solução: Erro IPv6 no Vercel

## ⚠️ Problema

O erro "Cannot assign requested address" com endereço IPv6 indica que o Vercel está tentando conectar via IPv6, o que pode causar problemas.

## ✅ Solução: Usar Connection Pooling (Porta 6543)

O Supabase oferece **Connection Pooling** que é mais confiável em ambientes serverless como o Vercel.

### Opção 1: Usar Variáveis Individuais com Pooling

**No Vercel, configure:**

```
DATABASE_TYPE=postgresql
USE_CONNECTION_POOLING=true
DB_HOST=db.htrghiefnoaytjmcdbuk.supabase.co
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=S&mur&i77681271
SUPABASE_URL=https://htrghiefnoaytjmcdbuk.supabase.co
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**Diferenças:**
- `USE_CONNECTION_POOLING=true` - Habilita pooling
- `DB_PORT=6543` - Porta de pooling (em vez de 5432)

### Opção 2: Usar DATABASE_URL com Pooling

**No Vercel, configure:**

```
DATABASE_URL=postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:6543/postgres?sslmode=require
DATABASE_TYPE=postgresql
SUPABASE_URL=https://htrghiefnoaytjmcdbuk.supabase.co
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**Importante:** A porta na URL deve ser **6543** (pooling) em vez de **5432** (direto).

## 📋 Como Obter a Connection String de Pooling

1. **Acesse o Supabase Dashboard**
   - Vá em: https://supabase.com/dashboard
   - Selecione seu projeto

2. **Vá em Settings → Database**
   - Role até **Connection Pooling**
   - Copie a **Connection String** (não a Connection String direta)
   - Ela já vem com a porta 6543

3. **Use no Vercel**
   - Adicione como `DATABASE_URL`
   - Certifique-se de que termina com `?sslmode=require`

## 🔍 Por Que Connection Pooling Funciona Melhor?

- ✅ **Mais confiável** em ambientes serverless
- ✅ **Melhor gerenciamento de conexões** (reutiliza conexões)
- ✅ **Menos problemas com IPv6/IPv4**
- ✅ **Otimizado para aplicações serverless** como Vercel

## 🧪 Testar

Após configurar:

1. **Faça um redeploy no Vercel**
2. **Acesse:** `https://seu-projeto.vercel.app/api/debug/banco`
3. **Verifique os logs** se ainda houver erro

## 📝 Nota sobre a Senha

Se sua senha contém caracteres especiais (como `&`), pode ser necessário usar URL encoding na `DATABASE_URL`:

- `&` → `%26`
- `#` → `%23`
- `@` → `%40`
- etc.

Ou use variáveis individuais (Opção 1), que não precisam de encoding.

