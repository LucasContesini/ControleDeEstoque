# Troubleshooting - Erro de Conexão com Banco no Vercel

## Erro: "Cannot assign requested address"

Este erro indica que o Vercel não consegue conectar ao Supabase PostgreSQL.

## Possíveis Causas e Soluções

### 1. Variáveis de Ambiente Não Configuradas

**Verifique se todas as variáveis estão configuradas no Vercel:**

1. Acesse: Dashboard do Vercel → Seu Projeto → Settings → Environment Variables
2. Verifique se estas variáveis estão configuradas:
   - `DATABASE_TYPE=postgresql`
   - `DB_HOST=db.htrghiefnoaytjmcdbuk.supabase.co`
   - `DB_PORT=5432`
   - `DB_NAME=postgres`
   - `DB_USER=postgres`
   - `DB_PASSWORD=S&mur&i77681271`

**Importante:** As variáveis devem estar configuradas para **todos os ambientes** (Production, Preview, Development).

### 2. Supabase Bloqueando Conexões do Vercel

O Supabase pode estar bloqueando conexões de IPs não autorizados.

**Solução:**
1. Acesse o dashboard do Supabase
2. Vá em **Settings** → **Database**
3. Em **Connection Pooling**, verifique as configurações
4. Em **Network Restrictions**, certifique-se de que não há restrições de IP que bloqueiem o Vercel

### 3. Connection String vs Variáveis Individuais

Se as variáveis individuais não funcionarem, tente usar uma connection string:

**No Vercel, adicione:**
```
DATABASE_URL=postgresql://postgres:S&mur&i77681271@db.htrghiefnoaytjmcdbuk.supabase.co:5432/postgres
```

E ajuste o `models.py` para usar `DATABASE_URL` se disponível.

### 4. Timeout de Conexão

O Vercel tem timeout de 10s (Hobby) ou 60s (Pro). Se a conexão demorar muito, pode falhar.

**Solução:** O código já tem `connect_timeout: 10` configurado.

### 5. SSL Requerido

O Supabase requer SSL. O código já tem `sslmode: 'require'` configurado.

## Teste de Conexão

Para testar se as variáveis estão corretas, adicione uma rota de teste:

```python
@app.route('/api/test-db', methods=['GET'])
def test_db():
    try:
        ensure_db_initialized()
        conn = get_db()
        cursor = get_cursor(conn)
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'status': 'ok', 'message': 'Conexão com banco OK'})
    except Exception as e:
        return jsonify({'status': 'erro', 'message': str(e)}), 500
```

Acesse: `https://seu-projeto.vercel.app/api/test-db`

## Verificar Logs

No dashboard do Vercel:
1. Vá em **Deployments**
2. Clique no deployment
3. Vá em **Functions** → `api/index.py`
4. Veja os logs para mais detalhes do erro

## Checklist

- [ ] Todas as variáveis de ambiente estão configuradas no Vercel
- [ ] Variáveis estão configuradas para todos os ambientes (Production, Preview, Development)
- [ ] Supabase não tem restrições de IP que bloqueiem o Vercel
- [ ] Senha do banco está correta (sem caracteres especiais mal escapados)
- [ ] Testou a conexão localmente com as mesmas credenciais

