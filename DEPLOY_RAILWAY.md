# Deploy no Railway - Controle de Estoque

## 🚀 Railway (Recomendado para Flask)

O Railway é a melhor opção para aplicações Flask, com suporte nativo e sem limitações de timeout.

## 📋 Passo a Passo

### 1. Criar conta no Railway
1. Acesse: https://railway.app
2. Faça login com GitHub
3. Clique em **New Project**

### 2. Conectar repositório
1. Selecione **Deploy from GitHub repo**
2. Escolha o repositório: `LucasContesini/ControleDeEstoque`
3. Railway detectará automaticamente que é Python

### 3. Configurar variáveis de ambiente
No dashboard do Railway, vá em **Variables** e adicione:

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

### 4. Configurar comando de start
No Railway, vá em **Settings** → **Deploy** e configure:

**Start Command:**
```bash
python app.py
```

Ou use Gunicorn (recomendado para produção):
```bash
pip install gunicorn && gunicorn app:app --host 0.0.0.0 --port $PORT
```

### 5. Deploy automático
- O Railway faz deploy automaticamente a cada push no GitHub
- Você receberá uma URL: `https://seu-projeto.up.railway.app`

## ✅ Vantagens do Railway

- ✅ Suporta Flask nativamente
- ✅ Sem timeout (diferente do Vercel)
- ✅ Uploads ilimitados
- ✅ Grátis para começar ($5 crédito/mês)
- ✅ Deploy automático do GitHub
- ✅ Logs em tempo real
- ✅ Variáveis de ambiente fáceis

## 📝 Arquivos Necessários

O projeto já tem tudo necessário:
- ✅ `requirements.txt` - Dependências
- ✅ `app.py` - Aplicação Flask
- ✅ Configuração pronta

## 🔧 Troubleshooting

### Erro: "Port not found"
- Adicione no `app.py`:
```python
import os
port = os.getenv('PORT', 5001)
app.run(host='0.0.0.0', port=int(port))
```

### Erro: "Module not found"
- Verifique se todas as dependências estão em `requirements.txt`

### Erro: "Database connection failed"
- Verifique variáveis de ambiente
- Confirme que o Supabase permite conexões externas

