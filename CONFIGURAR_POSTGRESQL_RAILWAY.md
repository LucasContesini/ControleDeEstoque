# 🗄️ Configurar PostgreSQL no Railway - Passo a Passo

## 📋 Passo 1: Criar Banco PostgreSQL no Railway

1. **No Dashboard do Railway:**
   - Clique em **New** (botão roxo no canto superior direito)
   - Selecione **Database** → **Add PostgreSQL**
   - O Railway criará automaticamente um banco PostgreSQL

2. **Aguardar Criação:**
   - O Railway levará alguns segundos para criar o banco
   - Você verá um card com o banco PostgreSQL criado

## 📋 Passo 2: Obter Credenciais

1. **Clique no banco PostgreSQL criado**
2. Vá na aba **Variables** (ou **Connect**)
3. Você verá as seguintes variáveis:
   - `PGHOST`
   - `PGPORT`
   - `PGDATABASE`
   - `PGUSER`
   - `PGPASSWORD`
   - `DATABASE_URL` (connection string completa)

## 📋 Passo 3: Conectar ao Web Service

### Opção A: Usar DATABASE_URL (Mais Simples) ⭐

1. **No seu Web Service no Railway:**
   - Vá em **Variables**
   - Clique em **+ New Variable**
   - **Name:** `DATABASE_URL`
   - **Value:** Copie o valor de `DATABASE_URL` do banco PostgreSQL
   - Clique em **Add**

2. **Adicione também:**
   ```
   DATABASE_TYPE=postgresql
   ```

3. **Mantenha as variáveis do Supabase Storage:**
   ```
   SUPABASE_URL=https://htrghiefnoaytjmcdbuk.supabase.co
   SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
   SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
   ```

### Opção B: Usar Variáveis Individuais

Se preferir usar variáveis individuais:

1. **No Web Service, adicione:**
   ```
   DATABASE_TYPE=postgresql
   DB_HOST=[valor de PGHOST do banco]
   DB_PORT=[valor de PGPORT do banco]
   DB_NAME=[valor de PGDATABASE do banco]
   DB_USER=[valor de PGUSER do banco]
   DB_PASSWORD=[valor de PGPASSWORD do banco]
   ```

## 📋 Passo 4: Deploy

1. **O Railway fará deploy automaticamente** após adicionar as variáveis
2. **Ou faça um Manual Deploy:**
   - Clique em **Deploy** → **Deploy Now**

## 📋 Passo 5: Migrar Dados (Se Necessário)

Se você já tem dados no Supabase e quer migrá-los:

### Exportar do Supabase:

1. **No Supabase Dashboard:**
   - Vá em **SQL Editor**
   - Execute:
   ```sql
   -- Exportar produtos
   COPY produtos TO STDOUT WITH CSV HEADER;
   ```

2. **Ou use pg_dump localmente:**
   ```bash
   pg_dump "postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:5432/postgres?sslmode=require" > backup.sql
   ```

### Importar no Railway:

1. **No Railway, vá no banco PostgreSQL**
2. Clique em **Connect** → **PostgreSQL Shell**
3. Execute o SQL exportado

**OU** use o Railway CLI:

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Conectar ao projeto
railway link

# Importar dados
railway run psql < backup.sql
```

## ✅ Checklist Final

- [ ] Banco PostgreSQL criado no Railway
- [ ] Variável `DATABASE_URL` adicionada ao Web Service
- [ ] Variável `DATABASE_TYPE=postgresql` adicionada
- [ ] Variáveis do Supabase Storage mantidas
- [ ] Deploy realizado
- [ ] Aplicação funcionando

## 🎉 Pronto!

Sua aplicação agora usa PostgreSQL do Railway, sem problemas de conectividade!

A URL será algo como: `https://seu-projeto.up.railway.app`


