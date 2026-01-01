# 🔧 Problema: IPv6 no Vercel - Soluções Alternativas

## ⚠️ Problema Atual

O Vercel está tentando conectar ao Supabase via IPv6 e falhando com "Cannot assign requested address", mesmo usando:
- ✅ Porta 6543 (connection pooling)
- ✅ IPv4 como fallback
- ✅ SSL configurado

## ✅ O Que Já Foi Implementado

1. **Detecção automática de Vercel** - O código detecta quando está no Vercel
2. **IPv4 primeiro** - Sempre tenta resolver e conectar via IPv4 primeiro no Vercel
3. **Connection pooling** - Usa porta 6543 por padrão no Vercel
4. **Fallbacks automáticos** - Tenta múltiplas abordagens se uma falhar

## 🔍 Possíveis Causas

1. **Supabase bloqueando conexões do Vercel**
   - Mesmo sem restrições de IP explícitas, pode haver bloqueio de rede

2. **Problema de DNS no Vercel**
   - O Vercel pode não conseguir resolver o hostname corretamente

3. **Firewall do Supabase**
   - Pode estar bloqueando conexões de certas regiões/IPs

## 🛠️ Soluções Alternativas

### Solução 1: Verificar Connection String do Supabase

No Supabase Dashboard:
1. Vá em **Settings** → **Database**
2. Role até **Connection Pooling**
3. Copie a **Connection String** completa
4. Use no Vercel como `DATABASE_URL`

A connection string do Supabase pode ter configurações especiais que funcionam melhor.

### Solução 2: Usar IPv4 Hardcoded (Temporário)

Se você conseguir o IPv4 do Supabase:

1. Execute localmente: `nslookup db.htrghiefnoaytjmcdbuk.supabase.co`
2. Pegue o IPv4 retornado
3. No `config.py`, altere temporariamente:
   ```python
   DB_HOST = '54.xxx.xxx.xxx'  # IPv4 do Supabase
   ```

⚠️ **Nota:** IPs podem mudar, então isso é temporário.

### Solução 3: Verificar se Supabase Está Acessível

Teste localmente se a conexão funciona:

```bash
psql "postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:6543/postgres?sslmode=require"
```

Se funcionar localmente mas não no Vercel, o problema é de rede/firewall.

### Solução 4: Contatar Suporte do Supabase

O problema pode ser específico do Supabase bloqueando conexões do Vercel. Contate o suporte do Supabase e pergunte:
- Se há bloqueios de rede para certas regiões
- Se há configurações especiais para serverless (Vercel)
- Se há whitelist de IPs necessária

### Solução 5: Usar Proxy/Tunnel (Último Recurso)

Como último recurso, você pode usar um serviço de proxy/tunnel, mas isso adiciona complexidade e latência.

## 📋 Checklist de Verificação

- [ ] Connection string do Supabase testada localmente
- [ ] IPv4 resolvido e testado
- [ ] Supabase Dashboard verificado (Network Restrictions)
- [ ] Logs do Vercel analisados
- [ ] Suporte do Supabase contatado (se necessário)

## 🔍 Debug no Vercel

Para ver mais detalhes:

1. **Acesse os logs do Vercel:**
   - Dashboard → Deployments → Functions → api/index.py
   - Veja os logs completos do erro

2. **Use a rota de debug:**
   - `https://seu-projeto.vercel.app/api/debug/banco`
   - Isso mostra informações de configuração

## 💡 Próximos Passos

1. **Teste localmente** com o script `testar_conexao_supabase.py`
2. **Verifique os logs do Vercel** para mais detalhes
3. **Tente a connection string completa** do Supabase Dashboard
4. **Contate o suporte do Supabase** se o problema persistir

O código já está otimizado para tentar IPv4 primeiro. Se ainda não funcionar, pode ser uma limitação de rede/firewall que precisa ser resolvida no lado do Supabase.

