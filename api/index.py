"""
Handler para Vercel Serverless Functions
Este arquivo expõe a aplicação Flask para o Vercel
"""
import sys
import os

# Adicionar o diretório raiz ao path para importar app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# O Vercel automaticamente detecta o objeto 'app' do Flask
# e o usa como handler WSGI

