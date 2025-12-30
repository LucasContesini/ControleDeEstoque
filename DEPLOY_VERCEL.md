# Deploy no Vercel - Controle de Estoque

## ⚠️ Importante sobre Vercel

O Vercel é otimizado para aplicações serverless e pode ter limitações com Flask. **Recomendamos usar Railway ou Render** para este projeto, que são mais adequados para aplicações Flask.

## 📋 Pré-requisitos

1. Conta no Vercel
2. Vercel CLI instalado: `npm i -g vercel`
3. Projeto conectado ao GitHub

## 🚀 Passo a Passo

### 1. Instalar Vercel CLI (se ainda não tiver)
```bash
npm i -g vercel
```

### 2. Fazer login no Vercel
```bash
vercel login
```

### 3. Configurar variáveis de ambiente no Vercel

No dashboard do Vercel, vá em **Settings** → **Environment Variables** e adicione:

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

### 4. Fazer deploy
```bash
vercel
```

Ou conecte diretamente ao GitHub no dashboard do Vercel.

## ⚠️ Limitações do Vercel com Flask

1. **Cold Start**: Pode haver delay na primeira requisição
2. **Timeout**: Funções têm timeout de 10s (Hobby) ou 60s (Pro)
3. **Upload de arquivos**: Pode ter limitações com uploads grandes
4. **Sessões**: Não mantém estado entre requisições

## 🔄 Alternativas Recomendadas

### Railway (Recomendado)
- ✅ Suporta Flask nativamente
- ✅ Sem timeout
- ✅ Uploads ilimitados
- ✅ Grátis para começar

**Deploy no Railway:**
1. Acesse: https://railway.app
2. Conecte seu repositório GitHub
3. Configure as variáveis de ambiente
4. Deploy automático!

### Render
- ✅ Suporta Flask
- ✅ Grátis (com limitações)
- ✅ Fácil configuração

**Deploy no Render:**
1. Acesse: https://render.com
2. New → Web Service
3. Conecte seu repositório
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --host 0.0.0.0 --port $PORT`
5. Adicione variáveis de ambiente
6. Deploy!

## 📝 Arquivos Necessários

O projeto já inclui:
- ✅ `vercel.json` - Configuração do Vercel
- ✅ `requirements.txt` - Dependências Python
- ✅ Handler serverless no `app.py`

## 🐛 Troubleshooting

### Erro: "Module not found"
- Verifique se todas as dependências estão em `requirements.txt`
- O Vercel instala automaticamente do `requirements.txt`

### Erro: "Timeout"
- Aumente o timeout no plano Pro do Vercel
- Ou considere usar Railway/Render

### Erro: "Database connection failed"
- Verifique se as variáveis de ambiente estão configuradas
- Confirme que o Supabase permite conexões externas

## 📚 Recursos

- [Vercel Python Documentation](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)

