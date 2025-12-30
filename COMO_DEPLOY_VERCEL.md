# 🚀 Como Fazer Deploy no Vercel - Passo a Passo

## ✅ Sim, dá para subir no Vercel!

O projeto já está configurado para funcionar no Vercel. Siga estes passos:

## 📋 Passo a Passo Completo

### 1. Instalar Vercel CLI (opcional, mas recomendado)
```bash
npm install -g vercel
```

### 2. Fazer login no Vercel
```bash
vercel login
```

### 3. Deploy via Dashboard (Mais Fácil) ⭐

1. **Acesse**: https://vercel.com
2. **Faça login** com GitHub
3. **Clique em**: "Add New..." → "Project"
4. **Importe** o repositório: `LucasContesini/ControleDeEstoque`
5. **Configure**:
   - Framework Preset: **Other**
   - Root Directory: `./` (raiz)
   - Build Command: (deixe vazio ou `pip install -r requirements.txt`)
   - Output Directory: (deixe vazio)
   - Install Command: `pip install -r requirements.txt`

### 4. Configurar Variáveis de Ambiente

No dashboard do Vercel, vá em **Settings** → **Environment Variables** e adicione:

```
DATABASE_TYPE = postgresql
DB_HOST = db.htrghiefnoaytjmcdbuk.supabase.co
DB_PORT = 5432
DB_NAME = postgres
DB_USER = postgres
DB_PASSWORD = S&mur&i77681271
SUPABASE_URL = https://htrghiefnoaytjmcdbuk.supabase.co
SUPABASE_KEY = sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY = sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

⚠️ **Importante**: Adicione para todos os ambientes (Production, Preview, Development)

### 5. Deploy!

Clique em **Deploy** e aguarde. O Vercel vai:
- Instalar dependências do `requirements.txt`
- Detectar que é Flask
- Fazer deploy automaticamente

### 6. Acessar sua aplicação

Após o deploy, você receberá uma URL tipo:
```
https://controle-de-estoque.vercel.app
```

## 🔧 Deploy via CLI (Alternativa)

Se preferir usar a linha de comando:

```bash
# No diretório do projeto
vercel

# Para produção
vercel --prod
```

## ⚠️ Limitações do Vercel (Importante Saber)

1. **Timeout**: 
   - Plano grátis: 10 segundos
   - Plano Pro: 60 segundos
   - Se sua aplicação demorar mais, vai dar timeout

2. **Cold Start**: 
   - Primeira requisição pode demorar alguns segundos
   - Normal em funções serverless

3. **Upload de Imagens**:
   - Pode ter limitações com arquivos muito grandes
   - Recomendado usar Supabase Storage (já configurado ✅)

4. **Sessões**:
   - Não mantém estado entre requisições
   - Mas seu app não usa sessões, então está OK ✅

## ✅ O que já está configurado

- ✅ `vercel.json` - Configuração do Vercel
- ✅ `requirements.txt` - Dependências Python
- ✅ `app.py` - Aplicação Flask pronta
- ✅ Porta dinâmica - Usa `$PORT` do ambiente

## 🐛 Troubleshooting

### Erro: "Module not found"
- Verifique se todas as dependências estão em `requirements.txt`
- O Vercel instala automaticamente

### Erro: "Timeout"
- Aumente o timeout no plano Pro
- Ou otimize o código para ser mais rápido

### Erro: "Database connection failed"
- Verifique se as variáveis de ambiente estão configuradas
- Confirme que o Supabase permite conexões externas

### Erro: "Port not found"
- O Vercel define automaticamente a porta
- O código já está configurado para usar `$PORT`

## 📝 Checklist Antes do Deploy

- [ ] Todas as dependências estão em `requirements.txt`
- [ ] Variáveis de ambiente configuradas no Vercel
- [ ] Repositório conectado ao GitHub
- [ ] `vercel.json` está na raiz do projeto
- [ ] Bucket "Controle de Estoque" criado no Supabase

## 🎉 Pronto!

Após seguir estes passos, sua aplicação estará no ar no Vercel!

**URL do seu projeto**: Será gerada automaticamente após o deploy.

---

## 💡 Dica

Se tiver problemas com timeout no Vercel, considere usar **Railway** ou **Render**, que são melhores para aplicações Flask contínuas.

