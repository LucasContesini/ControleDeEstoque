# 🧪 Como Testar Conexão com Supabase

## Script de Teste Automático

Criei um script que testa diferentes configurações para identificar qual funciona.

### Executar o Script

```bash
python3 testar_conexao_supabase.py
```

O script vai testar:
1. ✅ Resolução DNS (IPv4 e IPv6)
2. ✅ Conexão porta 5432 com SSL
3. ✅ Conexão porta 5432 sem SSL
4. ✅ Conexão porta 6543 (pooling) com SSL
5. ✅ Conexão porta 6543 (pooling) sem SSL
6. ✅ Connection strings com ambas as portas
7. ✅ Conexão direta via IPv4

### O Que o Script Mostra

O script mostrará qual configuração funciona e qual não funciona, ajudando a identificar:
- Se o problema é IPv6 vs IPv4
- Se pooling (6543) funciona melhor que direto (5432)
- Se SSL está causando problemas
- Qual é a melhor configuração para usar

## Melhorias no Código

O código agora tenta automaticamente:

1. **Conexão normal** (primeira tentativa)
2. **IPv4 direto** (se IPv6 falhar)
3. **Porta 6543** (pooling) como fallback se estiver usando 5432

## Próximos Passos

Após executar o script:

1. **Se pooling (6543) funcionar:**
   - Configure no Vercel: `DB_PORT=6543`
   - Ou use `DATABASE_URL` com porta 6543

2. **Se IPv4 funcionar:**
   - O código já tenta IPv4 automaticamente como fallback

3. **Se nada funcionar localmente:**
   - Verifique se o Supabase está acessível
   - Verifique se as credenciais estão corretas
   - Verifique se há restrições de firewall

## Configuração Recomendada no Vercel

Baseado nos testes, use:

```
DATABASE_TYPE=postgresql
DB_HOST=db.htrghiefnoaytjmcdbuk.supabase.co
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=S&mur&i77681271
SUPABASE_URL=https://htrghiefnoaytjmcdbuk.supabase.co
SUPABASE_KEY=sb_publishable_gSNmUBC5DQcx-UQKrFeGfw_wlbu27R9
SUPABASE_SERVICE_KEY=sb_secret_ZjnLl9_3WQzamHBRZHNFhw_J5q2xyhD
```

**Importante:** `DB_PORT=6543` (pooling) é mais confiável no Vercel.

