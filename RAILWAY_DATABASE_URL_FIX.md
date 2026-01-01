# 🔧 Corrigir Erro: "postgres.railway.internal" no Railway

## ⚠️ Problema

O Railway está usando a URL interna (`postgres.railway.internal`) que não funciona para serviços web.

## ✅ Solução: Usar URL Pública

### Opção 1: Obter URL Pública do Banco (Recomendado)

1. **No Railway, vá no banco PostgreSQL**
2. Clique na aba **Connect** ou **Public Networking**
3. Procure por **Public Connection String** ou **External Connection**
4. Copie essa URL (não a interna)
5. **No Web Service, atualize a variável `DATABASE_URL`** com essa URL pública

### Opção 2: Usar Variáveis Individuais

Se não encontrar a URL pública, use variáveis individuais:

1. **No banco PostgreSQL, vá em Variables**
2. Copie os valores de:
   - `PGHOST` (host público)
   - `PGPORT`
   - `PGDATABASE`
   - `PGUSER`
   - `PGPASSWORD`

3. **No Web Service, adicione/atualize:**
   ```
   DATABASE_TYPE=postgresql
   DB_HOST=[valor de PGHOST]
   DB_PORT=[valor de PGPORT]
   DB_NAME=[valor de PGDATABASE]
   DB_USER=[valor de PGUSER]
   DB_PASSWORD=[valor de PGPASSWORD]
   ```

4. **Remova ou deixe vazia a variável `DATABASE_URL`** (o código usará as individuais)

### Opção 3: Habilitar Public Networking

1. **No banco PostgreSQL no Railway:**
   - Vá em **Settings** ou **Networking**
   - Habilite **Public Networking** ou **External Access**
   - Isso gerará uma URL pública

2. **Use essa URL pública no `DATABASE_URL`**

## 🔍 Verificação

Após configurar, o `DATABASE_URL` deve conter um hostname público, não `railway.internal`.

Exemplo de URL pública:
```
postgresql://postgres:senha@containers-us-west-xxx.railway.app:5432/railway
```

NÃO deve ser:
```
postgresql://postgres:senha@postgres.railway.internal:5432/railway
```

## 📝 Nota

O código foi atualizado para tentar usar variáveis individuais quando detectar URL interna, mas a melhor solução é usar a URL pública do Railway.


