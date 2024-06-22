#Libraries
#from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#bibliotecas necessárias
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(
    page_title='Countries', page_icon='🌎', layout='wide')

#===================================================================================================================
#Funções
#===================================================================================================================

def bar_1(df):
    re2 = df.loc[:,['Restaurant ID','country']].groupby(['country']).count().sort_values(by='Restaurant ID',ascending=False).reset_index()
    fig = px.bar(re2, x='country',y='Restaurant ID',text_auto=True,labels={'country':'Países','Restaurant ID':'Quantidade de Restaurantes'},title='Quantidade de Restaurantes Registrados por País')
    return fig


def bar_2(df):
    re1 = df.loc[:,['country','City','Restaurant ID']].groupby(['country','City']).count().sort_values(by='country',ascending=False).reset_index()
    re1 = re1.loc[:,['country','City']].groupby(['country']).count().sort_values(by='City',ascending=False).reset_index()
    fig = px.bar(re1, x='country',y='City',text_auto=True,labels={'country':'Países','City':'Quantidade de Cidades'},title='Quantidade de Cidades Registradas por País')
    return fig


def bar_3(df):
    re8 = round(df.loc[:,['Votes','country']].groupby(['country']).mean().sort_values(by='Votes',ascending=False).reset_index(),2)
    fig = px.bar(re8, x='country',y='Votes',text_auto=True,labels={'country':'Países','Votes':'Quantidade de Avaliações'},title='Média de Avaliações feitas por País')
    return fig


def bar_4(df):
    re11 = round(df.loc[:,['Average Cost for two','country']].groupby(['country']).mean().sort_values(by='Average Cost for two',ascending=False).reset_index(),2)
    fig = px.bar(re11, x='country',y='Average Cost for two',text_auto=True,labels={'country':'Países','Average Cost for two':'Preço de prato para duas Pessoas'},title='Média do Preço de um prato para duas pessoas por País')
    return fig



#=============================Inicio da Estrutura Lógica do Código=====================================================
#================
#import dataset
#================
df = pd.read_csv(r'df_country.csv')


#===================================================================================================================
#Barra lateral
#===================================================================================================================
st.sidebar.markdown('## Filtros')

country = ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey']
country_op = st.sidebar.multiselect('Escolha os Países que Deseja visualizar as informações',
                      country,
                      default=['Brazil','England','Qatar', 'South Africa','Canada','Australia'])

df = df.loc[df['country'].isin(country_op),:]

st.sidebar.markdown ( """---""" )
st.sidebar.markdown( '### Powered by Comunidade DS' )


#===================================================================================================================
#Layout no Streamlit
#===================================================================================================================

st.markdown('# 🌎 Visão Países')

#Primeiro container com um gráfico
with st.container():
    fig = bar_1(df)
    st.plotly_chart(fig,use_container_width=True,theme=None)      

#Segundo container com um gráfico
with st.container():
    fig = bar_2(df)
    st.plotly_chart(fig,use_container_width=True,theme=None)

#Terceiro container com duas colunas, cada qual com um gráfico
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        fig = bar_3(df)
        st.plotly_chart(fig,use_container_width=True,theme=None)
                
    with col2:
        fig = bar_4(df)
        st.plotly_chart(fig,use_container_width=True,theme=None)
        









