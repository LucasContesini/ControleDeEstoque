# 📥 Como Importar Variáveis no Vercel

## Opção 1: Via Dashboard (Recomendado)

1. **Acesse o Vercel Dashboard**
   - Vá em: https://vercel.com/dashboard
   - Selecione seu projeto

2. **Vá em Settings → Environment Variables**

3. **Adicione cada variável:**
   - Clique em **Add New**
   - **Key:** `DB_PASSWORD`
   - **Value:** `S&mur&i77681271`
   - Selecione os ambientes (Production, Preview, Development)
   - Clique em **Save**
   
   Repita para:
   - `SUPABASE_KEY` = `sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9`
   - `SUPABASE_SERVICE_KEY` = `sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD`

## Opção 2: Via CLI (Mais Rápido)

Se você tem o Vercel CLI instalado:

```bash
# Fazer login (se ainda não fez)
vercel login

# Adicionar variáveis
vercel env add DB_PASSWORD
# Cole: S&mur&i77681271
# Selecione os ambientes (Production, Preview, Development)

vercel env add SUPABASE_KEY
# Cole: sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9

vercel env add SUPABASE_SERVICE_KEY
# Cole: sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

## Opção 3: Importar do Arquivo

O arquivo `vercel.env` contém todas as variáveis. Você pode:

1. **Copiar o conteúdo** do arquivo `vercel.env`
2. **Colar no Vercel Dashboard** (uma variável por vez)

Ou usar um script:

```bash
# Ler o arquivo e adicionar cada variável
cat vercel.env | grep -v '^#' | while IFS='=' read -r key value; do
  if [ ! -z "$key" ] && [ ! -z "$value" ]; then
    echo "Adicionando $key..."
    echo "$value" | vercel env add "$key" production preview development
  fi
done
```

## 📋 Variáveis Necessárias

Apenas estas 3 variáveis:

```
DB_PASSWORD=S&mur&i77681271
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

## ✅ Verificar

Após adicionar as variáveis:

1. **Faça um redeploy** no Vercel
2. **Acesse:** `https://seu-projeto.vercel.app/api/debug/banco`
3. **Verifique** se a conexão está funcionando

## 🔒 Segurança

⚠️ **Importante:**
- O arquivo `vercel.env` contém credenciais reais
- Ele está no `.gitignore` para não ser commitado
- Não compartilhe este arquivo publicamente
- Use apenas para importar no Vercel

