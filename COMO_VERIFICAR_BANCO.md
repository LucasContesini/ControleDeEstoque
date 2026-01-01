# 🔍 Como Verificar o Banco de Dados no Railway

## 📋 Opção 1: Executar Script Localmente

### 1. Configurar Variáveis de Ambiente

No terminal, configure as variáveis do Railway:

```bash
export DATABASE_TYPE=postgresql
export DB_HOST=switchyard.proxy.rlwy.net
export DB_PORT=20587
export DB_NAME=[seu PGDATABASE]
export DB_USER=[seu PGUSER]
export DB_PASSWORD=[seu PGPASSWORD]
```

Ou use `DATABASE_URL`:

```bash
export DATABASE_URL=postgresql://[user]:[password]@switchyard.proxy.rlwy.net:20587/[database]
```

### 2. Executar Script

```bash
python3 verificar_banco_railway.py
```

## 📋 Opção 2: Executar no Railway (Recomendado)

### 1. Via Railway CLI

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Conectar ao projeto
railway link

# Executar script
railway run python3 verificar_banco_railway.py
```

### 2. Via Dashboard do Railway

1. No Railway, vá no seu **Web Service**
2. Clique em **Shell** ou **Console**
3. Execute:
   ```bash
   python3 verificar_banco_railway.py
   ```

## 📋 Opção 3: Via API do Railway

Você também pode verificar diretamente pela aplicação:

1. Acesse: `https://seu-projeto.up.railway.app/api/produtos`
2. Veja se retorna JSON com os produtos
3. Verifique se os dados estão corretos

## ✅ O que o Script Verifica

- ✅ Conexão com o banco
- ✅ Existência da tabela `produtos`
- ✅ Estrutura da tabela (colunas)
- ✅ Total de produtos
- ✅ Primeiros 5 produtos com detalhes
- ✅ Tipos de dados (para detectar problemas)
- ✅ Dados problemáticos (valores NULL ou não numéricos)

## 🔧 Troubleshooting

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

### Erro: "Connection failed"
- Verifique se as variáveis de ambiente estão configuradas
- Confirme que o host e porta estão corretos

### Erro: "Table not found"
- Execute a inicialização do banco primeiro
- A aplicação cria a tabela automaticamente na primeira requisição


