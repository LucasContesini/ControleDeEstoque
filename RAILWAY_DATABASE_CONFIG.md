# 🔧 Configuração do Banco PostgreSQL no Railway

## ✅ URL Pública do Banco

Você forneceu:
- **Host:** `switchyard.proxy.rlwy.net`
- **Porta:** `20587`

## 📋 Configuração no Railway

### No Web Service, configure estas variáveis:

#### Opção 1: Usar DATABASE_URL (Recomendado)

Você precisa montar a connection string completa. No Railway:

1. **Vá no banco PostgreSQL → Variables**
2. Copie os valores de:
   - `PGDATABASE` (nome do banco)
   - `PGUSER` (usuário)
   - `PGPASSWORD` (senha)

3. **No Web Service, atualize `DATABASE_URL` com:**
   ```
   DATABASE_URL=postgresql://[PGUSER]:[PGPASSWORD]@switchyard.proxy.rlwy.net:20587/[PGDATABASE]
   ```

   **Exemplo:**
   ```
   DATABASE_URL=postgresql://postgres:senha123@switchyard.proxy.rlwy.net:20587/railway
   ```

#### Opção 2: Usar Variáveis Individuais

**No Web Service, adicione/atualize:**

```
DATABASE_TYPE=postgresql
DB_HOST=switchyard.proxy.rlwy.net
DB_PORT=20587
DB_NAME=[valor de PGDATABASE do banco]
DB_USER=[valor de PGUSER do banco]
DB_PASSWORD=[valor de PGPASSWORD do banco]
```

## 🔍 Como Obter as Credenciais

1. **No Railway, clique no banco PostgreSQL**
2. Vá em **Variables**
3. Você verá:
   - `PGDATABASE` - nome do banco
   - `PGUSER` - usuário (geralmente `postgres`)
   - `PGPASSWORD` - senha
   - `PGHOST` - host (pode ser o interno, ignore)
   - `PGPORT` - porta (pode ser diferente, use a pública: 20587)

## ✅ Checklist

- [ ] Host público: `switchyard.proxy.rlwy.net` ✅
- [ ] Porta pública: `20587` ✅
- [ ] Nome do banco (PGDATABASE)
- [ ] Usuário (PGUSER)
- [ ] Senha (PGPASSWORD)
- [ ] `DATABASE_TYPE=postgresql`

## 🎯 Próximo Passo

Após configurar, faça um deploy e teste a conexão!

