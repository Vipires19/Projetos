import os
import re
import openai
import streamlit as st
import pickle
from dotenv import load_dotenv,find_dotenv
from unidecode import unidecode
from pathlib import Path

_ = load_dotenv(find_dotenv())
pasta_mensagens = Path(__file__).parent / 'conversas_salvas'
pasta_mensagens.mkdir(exist_ok=True)

client = openai.Client()

def resposta_chat(mensagens):
    respostas = client.chat.completions.create(
        messages = mensagens,
        model = 'gpt-3.5-turbo-0125',
        max_tokens = 1000,
        temperature = 0,
        stream = True,
    )           
    return respostas

def converte_nome(nome_mensagem):
    nome_arquivo = unidecode(nome_mensagem)
    nome_arquivo = re.sub('\W+', '', nome_arquivo).lower()
    return nome_arquivo

def set_nome_msg(mensagens):
    nome_mensagem = ''
    for mensagem in mensagens:
        if mensagem['role'] == 'user':
            nome_mensagem = mensagem['content'][:30]
            break
    return nome_mensagem

def salva_mensagens(mensagens):
    if len(mensagens) == 0:
        return False
    nome_mensagem = set_nome_msg(mensagens)
    nome_arquivo = converte_nome(nome_mensagem)
    arquivo_salvar = {'nome_mensagem' : nome_mensagem, 
                      'nome_arquivo' : nome_arquivo,
                      'mensagens' : mensagens}
    with open(pasta_mensagens / nome_arquivo, 'wb') as f:
        pickle.dump(arquivo_salvar, f)

def ler_arquivo(mensagens, key = 'mensagem'):
    if len(mensagens) == 0:
        return []
    nome_mensagem = set_nome_msg(mensagens)
    nome_arquivo = converte_nome(nome_mensagem)
    with open(pasta_mensagens / nome_arquivo, 'rb') as f:
        mensagens = pickle.load(f)
    return mensagens[key]

def pagina_principal():

    if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []

    mensagens = ler_arquivo(st.session_state.mensagens)
    st.header('🤖 PirécoBot', divider = True)

    for mensagem in mensagens:
        chat = st.chat_message(mensagem['role'])
        chat.markdown(mensagem['content'])

    prompt = st.chat_input("Fale como Piréco")
    if prompt:
        nova_mensagem = ({'role': 'user', 'content': prompt})
        chat = st.chat_message(nova_mensagem['role'])
        chat.markdown(nova_mensagem['content'])
        mensagens.append(nova_mensagem)
        st.session_state.mensagens = mensagens

        chat = st.chat_message('assistant')
        placeholder = chat.empty()
        placeholder.markdown('⎸')
        resposta_completa = ''
        respostas = resposta_chat(mensagens)
        for resposta in respostas:
            texto = resposta.choices[0].delta.content
            if texto:
                resposta_completa += texto
                print(texto, end = '')
            placeholder.markdown(resposta_completa + '⎸')
            placeholder.markdown(resposta_completa)
        nova_mensagem = {'role': 'assistant', 'content': resposta_completa}
        mensagens.append(nova_mensagem)
        
        st.session_state.mensagens = mensagens
        salva_mensagens(mensagens)

pagina_principal()