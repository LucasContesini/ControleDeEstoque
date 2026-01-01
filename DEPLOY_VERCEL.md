# Deploy no Vercel - Controle de Estoque

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
- Otimize o código para ser mais rápido

### Erro: "Database connection failed"
- Verifique se as variáveis de ambiente estão configuradas
- Confirme que o Supabase permite conexões externas

## 📚 Recursos

- [Vercel Python Documentation](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)

