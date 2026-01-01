# ⚡ Configuração Simplificada - Vercel

## ✅ Agora Apenas 3 Variáveis!

A configuração foi simplificada. A maioria dos valores está hardcoded no arquivo `config.py`.

## 📋 Variáveis no Vercel (Apenas 3!)

No **Vercel Dashboard** → **Settings** → **Environment Variables**, adicione apenas:

```
DB_PASSWORD=S&mur&i77681271
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**Pronto!** Não precisa configurar mais nada.

## 🔧 O Que Está Hardcoded

As seguintes configurações estão no arquivo `config.py` e não precisam ser configuradas:

- ✅ `DB_HOST` = `db.htrghiefnoaytjmcdbuk.supabase.co`
- ✅ `DB_PORT` = `6543` (connection pooling)
- ✅ `DB_NAME` = `postgres`
- ✅ `DB_USER` = `postgres`
- ✅ `SUPABASE_URL` = `https://htrghiefnoaytjmcdbuk.supabase.co`
- ✅ `BUCKET_NAME` = `Controle de Estoque`
- ✅ `DATABASE_TYPE` = Detectado automaticamente

## 📝 Checklist

- [ ] `DB_PASSWORD` configurada
- [ ] `SUPABASE_KEY` configurada
- [ ] `SUPABASE_SERVICE_KEY` configurada
- [ ] Variáveis configuradas para **todos os ambientes** (Production, Preview, Development)
- [ ] Redeploy feito após configurar

## 🧪 Testar

Após configurar e fazer redeploy:

```
https://seu-projeto.vercel.app/api/debug/banco
```

## 💡 Vantagens

- ✅ **Muito mais simples** - apenas 3 variáveis
- ✅ **Menos erros** - valores hardcoded não podem ser configurados errado
- ✅ **Mais rápido** - menos configuração
- ✅ **Fácil de manter** - tudo centralizado em `config.py`

## 🔄 Se Precisar Mudar Valores

Se precisar mudar algum valor hardcoded (ex: host, porta), edite o arquivo `config.py` e faça commit.

