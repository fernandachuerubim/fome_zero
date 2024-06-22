import streamlit as st
import os
from PIL import Image

st.set_page_config(
    page_title="Home")

#image_path = 'C:\Users\Admin\Downloads\FTC\'
image = Image.open( 'logo.jpg' )
st.sidebar.image( image )

st.sidebar.markdown( '# Fome Zero' )
st.sidebar.markdown( """---""" )

st.write( "#Fome Zero!" )

st.markdown(
    """
    O melhor lugar para encontrar seu mais novo restaurante favorito!
    ### Temos os seguintes Dashboards:
    - Visão Geral
    - Visão Países
    - Visão Tipos de Culinárias
    - Visão Cidades
    ### Ask for Help
    - Time de Data Science no Discord
        - @fernanda.3458
""")