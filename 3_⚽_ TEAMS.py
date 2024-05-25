import streamlit as st
import pandas as pd


df = st.session_state['data']

clubes = df['Club'].value_counts().index
club = st.sidebar.selectbox('Clubes', clubes)

df_filtrado = df[(df['Club'] == club)].set_index('Name')

st.image(df_filtrado.iloc[0]['Club Logo'])
st.markdown(f'**{club}**')

colunas = ['Age','Photo','Flag','Overall','Value(£)','Wage(£)','Position','Contract Valid Until','Kit Number']

st.dataframe(df_filtrado[colunas],
             column_config={'Photo': st.column_config.ImageColumn(),
                            'Flag': st.column_config.ImageColumn('Country'),
                            'Overall': st.column_config.ProgressColumn(format="%f"),
                            'Wage(£)': st.column_config.ProgressColumn('Weekly Wage', format= '£%f', min_value=0, max_value=df_filtrado['Wage(£)'].max())})