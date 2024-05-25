import streamlit as st
import pandas as pd
import webbrowser
from datetime import datetime

if 'data' not in st.session_state:
    df = pd.read_csv(r'C:\Users\user\Downloads\Data science\Python\Streamlit\Projeto Streamlit FIFA\datasets\CLEAN_FIFA23_official_data.csv')
    df = df[df['Contract Valid Until'] >= datetime.today().year]
    df = df[df["Value(£)"] > 0]
    df = df.sort_values(by= 'Overall', ascending= False)
    st.session_state['data'] = df


st.set_page_config(
    layout =  'wide',
    page_title = 'HOME',
    page_icon = '🏠'
)

st.markdown('# FIFA 23 OFICIAL DATASET ⚽')
btn = st.button('ACESSE OS DADOS')
if btn:
    webbrowser.open_new_tab('https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data')

st.markdown(
    """
    O conjunto de dados
    de jogadores de futebol de 2017 a 2023 fornece informações 
    abrangentes sobre jogadores de futebol profissionais.
    O conjunto de dados contém uma ampla gama de atributos, incluindo dados demográficos 
    do jogador, características físicas, estatísticas de jogo, detalhes do contrato e 
    afiliações de clubes. 
    
    Com **mais de 17.000 registros**, este conjunto de dados oferece um recurso valioso para 
    analistas de futebol, pesquisadores e entusiastas interessados em explorar vários 
    aspectos do mundo do futebol, pois permite estudar atributos de jogadores, métricas de 
    desempenho, avaliação de mercado, análise de clubes, posicionamento de jogadores e 
    desenvolvimento do jogador ao longo do tempo.
"""
)

#st.cache_data
#def load_data():
#    df = pd.read_csv(r'C:\Users\user\Downloads\Data science\Python\Streamlit\Curso Streamlit\01 Spotify.csv')
#    return df