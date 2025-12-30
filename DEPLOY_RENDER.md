# Deploy no Render - Controle de Estoque

## 🚀 Passo a Passo Completo

### 1. Criar Web Service

1. Acesse: https://render.com
2. Faça login com GitHub
3. Clique em **New** → **Web Service**
4. Conecte o repositório: `LucasContesini/ControleDeEstoque`

### 2. Configurações do Web Service

Preencha os campos:

- **Name**: `controle-de-estoque` (ou o nome que preferir)
- **Region**: Escolha a mais próxima (ex: `Oregon (US West)`)
- **Branch**: `master`
- **Root Directory**: (deixe vazio)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

⚠️ **IMPORTANTE**: Use `--bind 0.0.0.0:$PORT` ao invés de `--host` e `--port` separados!

### 3. Variáveis de Ambiente

No Render, vá em **Environment** e adicione:

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

### 4. Deploy

Clique em **Create Web Service** e aguarde o deploy (pode levar alguns minutos).

## ✅ Comandos Corretos

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

## 🔧 Troubleshooting

### Erro: "gunicorn: command not found"
- ✅ Já corrigido: `gunicorn` está no `requirements.txt`

### Erro: "unrecognized arguments: --host"
- ✅ Use `--bind 0.0.0.0:$PORT` ao invés de `--host` e `--port`

### Erro de conexão com banco
- Verifique se todas as variáveis de ambiente estão configuradas
- Confirme que o Supabase permite conexões externas

## 📝 Notas

- O Render usa a variável `$PORT` automaticamente
- O `gunicorn` já está no `requirements.txt`
- O deploy é automático a cada push no GitHub

## 🎉 Pronto!

Após o deploy, sua aplicação estará disponível em:
`https://controle-de-estoque.onrender.com`

