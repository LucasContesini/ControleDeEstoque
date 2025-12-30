# 🔧 Como Corrigir o Erro de Python 3.13 no Render

## ⚠️ Problema

O Render está usando Python 3.13, mas `psycopg2-binary` não é compatível com essa versão.

## ✅ Solução: Configurar Python 3.12 Manualmente

### Passo a Passo:

1. **Acesse o Dashboard do Render**
   - Vá em: https://dashboard.render.com
   - Selecione seu Web Service: `controle-de-estoque`

2. **Vá em Settings**
   - Clique na aba "Settings" no menu lateral

3. **Configure a Versão do Python**
   - Role até a seção "Environment"
   - Procure por "Python Version" ou "Runtime"
   - **Selecione: `Python 3.12.7`** (ou qualquer versão 3.12.x)
   - **NÃO use Python 3.13**

4. **Salve as Alterações**
   - Clique em "Save Changes"

5. **Faça Deploy Manual**
   - Vá em "Manual Deploy" no menu superior
   - Selecione "Deploy latest commit"
   - Aguarde o build completar

## 📝 Verificação

Após o deploy, verifique os logs. Você deve ver algo como:
```
Python 3.12.7
```

E **NÃO** deve ver:
```
Python 3.13
```

## 🔄 Se Não Funcionar

Se ainda estiver usando Python 3.13 após configurar:

1. **Delete o Web Service atual**
2. **Crie um novo Web Service**
3. **Durante a criação, especifique Python 3.12.7**
4. **Ou use o `render.yaml` que já está no repositório**

## 📋 Arquivos Criados

- ✅ `runtime.txt` - Especifica Python 3.12.7
- ✅ `render.yaml` - Configuração completa com Python 3.12.7

Mas o Render pode não detectar automaticamente. **Configure manualmente no dashboard!**

