# 🔧 Troubleshooting - Erro de Conexão no Railway

## Erro: "Network is unreachable"

Este erro indica que o Railway não consegue conectar ao Supabase PostgreSQL.

## ✅ Soluções

### 1. Verificar Configurações do Supabase

No dashboard do Supabase:

1. **Settings** → **Database**
2. Verifique se há **restrições de IP** que bloqueiem conexões externas
3. Em **Connection Pooling**, certifique-se de que está habilitado
4. Em **Network Restrictions**, remova qualquer restrição que bloqueie o Railway

### 2. Usar Connection Pooling (Recomendado)

O Supabase oferece uma URL de connection pooling que é mais confiável:

1. No Supabase, vá em **Settings** → **Database**
2. Role até **Connection Pooling**
3. Copie a **Connection String** (não a Connection String direta)
4. Use o formato: `postgresql://postgres:[PASSWORD]@[HOST]:6543/postgres`

**No Railway, adicione uma nova variável:**
```
DATABASE_URL=postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:6543/postgres?sslmode=require
```

E ajuste o `models.py` para usar `DATABASE_URL` se disponível.

### 3. Verificar Variáveis de Ambiente no Railway

Certifique-se de que todas as variáveis estão configuradas:

```
DATABASE_TYPE=postgresql
DB_HOST=db.htrghiefnoaytjmcdbuk.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=S&mur&i77681271
SUPABASE_URL=https://htrghiefnoaytjmcdbuk.supabase.co
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

### 4. Testar Conexão Localmente

Teste se a conexão funciona localmente:

```bash
psql "postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:5432/postgres?sslmode=require"
```

Se funcionar localmente mas não no Railway, o problema é de rede/firewall.

### 5. Verificar Logs do Railway

No Railway:
1. Vá em seu serviço
2. Clique em **Logs**
3. Veja se há mais detalhes do erro

### 6. Usar Connection String Completa

Em vez de variáveis separadas, use uma connection string:

**No Railway, adicione:**
```
DATABASE_URL=postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:5432/postgres?sslmode=require
```

E modifique o `models.py` para usar `DATABASE_URL` se disponível.

## 🔍 Verificação Rápida

1. ✅ Variáveis de ambiente configuradas no Railway?
2. ✅ Supabase permite conexões externas?
3. ✅ SSL está configurado (`sslmode=require`)?
4. ✅ Senha está correta (sem caracteres especiais mal escapados)?

## 💡 Alternativa: Usar PostgreSQL do Railway

Se o problema persistir, você pode criar um banco PostgreSQL diretamente no Railway:

1. No Railway, clique em **New** → **Database** → **Add PostgreSQL**
2. Railway criará um banco PostgreSQL
3. Use as credenciais fornecidas pelo Railway
4. Migre os dados do Supabase para o Railway (se necessário)

## 📚 Recursos

- [Supabase Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
- [Railway Database](https://docs.railway.app/databases/postgresql)

