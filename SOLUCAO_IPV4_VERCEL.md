# ✅ Solução: Vercel é IPv4-only - Use Session/Transaction Pooler

## 🎯 Problema Identificado

O Supabase mostra claramente que:
- **Vercel é IPv4-only** (não suporta IPv6)
- **Direct Connection (porta 5432) não funciona** com IPv4-only platforms
- **Solução:** Usar **Session Pooler** ou **Transaction Pooler**

## ✅ Solução: Usar Connection String do Pooler

No Supabase Dashboard:

1. **Vá em Settings → Database**
2. **Role até Connection Pooling**
3. **Copie a Connection String** do **Session Pooler** ou **Transaction Pooler**
   - Não use a "Direct Connection"
   - Use a connection string do pooler (geralmente porta diferente ou configuração especial)

## 📋 Configuração no Vercel

### Opção 1: Usar DATABASE_URL (Recomendado)

No Vercel, adicione apenas:

```
DATABASE_URL=[Connection String do Session/Transaction Pooler do Supabase]
DB_PASSWORD=S&mur&i77681271
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**Importante:** Use a connection string completa do pooler que o Supabase fornece, não construa manualmente.

### Opção 2: Verificar Porta do Pooler

O pooler pode usar uma porta diferente. Verifique no Supabase Dashboard qual porta o Session/Transaction Pooler usa e configure:

```
DB_HOST=[host do pooler]
DB_PORT=[porta do pooler - pode ser diferente de 5432/6543]
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=S&mur&i77681271
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

## 🔍 Como Obter a Connection String Correta

1. **Acesse:** https://supabase.com/dashboard
2. **Selecione seu projeto**
3. **Vá em:** Settings → Database
4. **Role até:** Connection Pooling
5. **Procure por:** "Session Pooler" ou "Transaction Pooler"
6. **Copie a Connection String** fornecida (não a Direct Connection)

A connection string do pooler já vem configurada para funcionar com IPv4-only platforms como Vercel.

## ⚠️ Diferença Entre Poolers

- **Direct Connection (5432):** ❌ Não funciona com Vercel (IPv4-only)
- **Session Pooler:** ✅ Funciona com Vercel (IPv4-compatible)
- **Transaction Pooler (6543):** ✅ Funciona com Vercel (IPv4-compatible)
- **Connection Pooler (6543):** Pode funcionar, mas Session/Transaction são recomendados

## 🚀 Próximos Passos

1. **Copie a Connection String do Session/Transaction Pooler** do Supabase Dashboard
2. **Adicione no Vercel como `DATABASE_URL`**
3. **Faça redeploy**
4. **Teste:** `https://seu-projeto.vercel.app/api/debug/banco`

## 💡 Nota

O código já está preparado para usar `DATABASE_URL` se disponível. Basta copiar a connection string correta do Supabase Dashboard e configurar no Vercel.

