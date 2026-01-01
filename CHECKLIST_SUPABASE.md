# ✅ Checklist de Configuração do Supabase

## Configurações Verificadas

### 1. Network Restrictions ✅
- **Status:** "Your database can be accessed by all IP addresses"
- **Ação:** ✅ Correto - Sem restrições de IP
- **Nota:** Isso permite que o Vercel (com IPs dinâmicos) se conecte

### 2. SSL Configuration ⚠️
- **Status:** "Enforce SSL on incoming connections" está **DESLIGADO**
- **Ação:** ⚠️ Opcional - Pode deixar desligado se usar `sslmode=require` na connection string
- **Recomendação:** 
  - Se quiser mais segurança, pode ligar o toggle
  - Mas o código já usa `sslmode=require`, então está OK assim

### 3. Connection Pooling ✅
- **Pool Size:** 15 conexões (padrão para Nano)
- **Max Client Connections:** 200 (fixo para Nano)
- **Status:** ✅ Configuração adequada para o projeto

## Próximos Passos

1. **Verificar variáveis no Vercel:**
   - Certifique-se de que todas as variáveis estão configuradas
   - Especialmente `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

2. **Testar conexão:**
   - Após configurar as variáveis no Vercel, faça um redeploy
   - Acesse: `https://seu-projeto.vercel.app/api/debug/banco`

3. **Se ainda der erro:**
   - Verifique os logs do Vercel
   - Confirme que a senha está correta (sem caracteres especiais mal escapados)
   - Tente usar `DATABASE_URL` em vez de variáveis individuais

## Variáveis Necessárias no Vercel

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

## Troubleshooting

Se o erro "Cannot assign requested address" persistir:

1. **Teste a connection string localmente:**
   ```bash
   psql "postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:5432/postgres?sslmode=require"
   ```

2. **Use DATABASE_URL no Vercel:**
   ```
   DATABASE_URL=postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:5432/postgres?sslmode=require
   ```

3. **Verifique se o bucket do Storage existe:**
   - Vá em Storage no Supabase
   - Certifique-se de que o bucket "Controle de Estoque" existe e está público

