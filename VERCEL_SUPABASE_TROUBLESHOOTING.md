# 🔧 Troubleshooting: Vercel + Supabase

## ⚠️ Erro: "Cannot assign requested address"

Este erro indica que o Vercel não consegue conectar ao Supabase PostgreSQL.

## ✅ Soluções (em ordem de prioridade)

### 1. Verificar Restrições de Rede no Supabase

O Supabase pode ter restrições de IP que bloqueiam conexões do Vercel.

**Passos:**

1. **Acesse o Supabase Dashboard**
   - Vá em: https://supabase.com/dashboard
   - Selecione seu projeto

2. **Vá em Settings → Database**
   - Role até a seção **Network Restrictions**

3. **Remova todas as restrições de IP** (ou adicione os IPs do Vercel)
   - O Vercel usa IPs dinâmicos, então é melhor **remover todas as restrições**
   - Clique em **Remove** ou **Clear all restrictions**

4. **Salve as alterações**

### 2. Verificar Variáveis de Ambiente no Vercel

Certifique-se de que todas as variáveis estão configuradas corretamente:

**No Vercel Dashboard:**
1. Vá em seu projeto
2. Clique em **Settings** → **Environment Variables**
3. Adicione/verifique as seguintes variáveis:

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

**⚠️ Importante:**
- Use as credenciais corretas do seu projeto Supabase
- Não use espaços antes ou depois dos valores
- Certifique-se de que não há aspas extras

### 3. Usar Connection String (Alternativa)

Se preferir usar uma connection string completa:

**No Vercel, adicione:**
```
DATABASE_URL=postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:5432/postgres?sslmode=require
```

**Formato:**
```
postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]?sslmode=require
```

**⚠️ Substitua:**
- `[USER]` pelo seu usuário (geralmente `postgres`)
- `[PASSWORD]` pela sua senha
- `[HOST]` pelo host do Supabase (ex: `db.xxxxx.supabase.co`)
- `[PORT]` pela porta (geralmente `5432`)
- `[DATABASE]` pelo nome do banco (geralmente `postgres`)

### 4. Verificar Connection Pooling (Opcional)

O Supabase oferece connection pooling que pode ser mais confiável:

1. **No Supabase Dashboard:**
   - Vá em **Settings** → **Database**
   - Role até **Connection Pooling**
   - Copie a **Connection String** (porta 6543)

2. **No Vercel, use:**
   ```
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:6543/postgres?sslmode=require
   ```

### 5. Verificar Logs do Vercel

Para ver mais detalhes do erro:

1. **No Vercel Dashboard:**
   - Vá em seu projeto
   - Clique em **Deployments**
   - Clique no deployment mais recente
   - Clique em **Functions** → **api/index.py**
   - Veja os logs de erro

### 6. Testar Conexão Localmente

Teste se a conexão funciona localmente:

```bash
# Instalar psql (se não tiver)
# macOS: brew install postgresql
# Linux: sudo apt-get install postgresql-client

# Testar conexão
psql "postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:5432/postgres?sslmode=require"
```

Se funcionar localmente mas não no Vercel, o problema é de rede/firewall do Supabase.

### 7. Verificar SSL

O Supabase **requer SSL** para conexões externas. O código já está configurado para usar `sslmode=require`, mas verifique:

- Se usar `DATABASE_URL`, certifique-se de que termina com `?sslmode=require`
- Se usar variáveis individuais, o código adiciona `sslmode=require` automaticamente

## 📋 Checklist de Verificação

- [ ] Restrições de IP removidas no Supabase
- [ ] Variáveis de ambiente configuradas no Vercel
- [ ] `DATABASE_TYPE=postgresql` está definido
- [ ] Credenciais do Supabase estão corretas
- [ ] SSL está habilitado (`sslmode=require`)
- [ ] Porta está correta (5432 para direto, 6543 para pooling)
- [ ] Host está correto (sem `http://` ou `https://`)

## 🔍 Debug

Para debugar, acesse a rota de debug:

```
https://seu-projeto.vercel.app/api/debug/banco
```

Isso mostrará informações detalhadas sobre a conexão e possíveis problemas.

## 📞 Ainda com Problemas?

Se após seguir todos os passos o problema persistir:

1. **Verifique os logs do Vercel** para ver o erro completo
2. **Teste a conexão localmente** com `psql`
3. **Verifique se o Supabase está online** (dashboard do Supabase)
4. **Tente usar connection pooling** (porta 6543) em vez de conexão direta

