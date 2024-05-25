import streamlit as st
import pandas as pd

df = st.session_state['data']

clubes = df['Club'].value_counts().index
club = st.sidebar.selectbox('Clubes', clubes)
df_players = df[df['Club'] == club]
jogadores = df_players['Name'].value_counts().index
jogador = st.sidebar.selectbox('Jogador', jogadores)

player_stats = df[df['Name'] == jogador].iloc[0]

st.image(player_stats['Photo'])
st.title(player_stats['Name'])
st.markdown(f'**Clube**: {player_stats["Club"]}')
st.markdown(f'**Posição**: {player_stats["Position"]}')

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'**Idade**: {player_stats["Age"]}')
col2.markdown(f'**Altura**: {player_stats["Height(cm.)"] / 100}')
col3.markdown(f'**Peso**: {player_stats["Weight(lbs.)"] * 0.453 :.2f}')
col4.markdown(f'**Pé Preferido**: {player_stats["Preferred Foot"]}')

st.divider()

st.subheader(f'Overall: {player_stats["Overall"]}')
st.progress(int(player_stats["Overall"]))

col1,col2,col3 = st.columns(3)
col1.metric(label='Valor de Mercado', value=f'£ {player_stats["Value(£)"]:,}')
col2.metric(label='Remuneração Semanal', value=f'£ {player_stats["Wage(£)"]:,}')
col3.metric(label='Claúsula de Rescição', value=f'£ {player_stats["Release Clause(£)"]:,}')