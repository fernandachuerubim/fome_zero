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
import inflection

st.set_page_config(
    page_title='Cities', page_icon='🏙️', layout='wide')


#===================================================================================================================
#Funções
#===================================================================================================================


def bar_1(df):
    re1 = df.loc[:,['country','City','Restaurant ID']].groupby(['country','City']).count().sort_values(by=['Restaurant ID','City'],ascending=[False,True]).reset_index()
    fig = px.bar(re1.head(10), x='City',y='Restaurant ID',text_auto=True,labels={'City':'Cidade','Restaurant ID':'Quantidade de Restaurantes','country':'País',},color='country',title='Top 10 Cidades com mais Restaurantes na Base de Dados')
    return fig


def bar_2(df):
    re2 = df.loc[:,['country','City','Aggregate rating','Restaurant ID']].groupby(['country','City','Restaurant ID']).mean().sort_values(by=['Restaurant ID','City'],ascending=[False,True]).reset_index()
    re2 = re2.loc[re2['Aggregate rating'] >= 4,['country','City','Restaurant ID']].groupby(['country','City']).count().sort_values(by=['Restaurant ID','City'],ascending=[False,True]).reset_index()
    fig = px.bar(re2.head(7), x='City',y='Restaurant ID',text_auto=True,labels={'City':'Cidade','Restaurant ID':'Quantidade de Restaurantes','country':'País'},color='country',title='Top 7 Cidades com Restaurantes com média de avaliação acima de 4')
    return fig
    

def bar_3(df):
    re2 = df.loc[:,['country','City','Aggregate rating','Restaurant ID']].groupby(['country','City','Restaurant ID']).mean().sort_values(by=['Restaurant ID','City'],ascending=[False,True]).reset_index()
    re2 = re2.loc[re2['Aggregate rating'] <= 2.5,['country','City','Restaurant ID']].groupby(['country','City']).count().sort_values(by=['Restaurant ID','City'],ascending=[False,True]).reset_index()
    fig = px.bar(re2.head(7), x='City',y='Restaurant ID',text_auto=True,labels={'City':'Cidade','Restaurant ID':'Quantidade de Restaurantes','country':'País'},color='country',title='Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5')
    return fig


def bar_4(df):
    re5 = df.loc[:,['country','City','Cuisines','Restaurant ID']].groupby(['country','City','Cuisines']).count().sort_values(by=['Restaurant ID'],ascending=[False]).reset_index()
    re5 = re5.loc[:,['country','City','Cuisines']].groupby(['country','City']).count().sort_values(by=['Cuisines','City','country'],ascending=[False,True,True]).reset_index()
    fig = px.bar(re5.head(10), x='City',y='Cuisines',text_auto=True,labels={'City':'Cidade','Cuisines':'Quantidade de Tipos Culinários Únicos','country':'País'},color='country',title='Top 10 Cidades mais restaurantes com tipos culinários distintos')
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


st.markdown('# 🏙️ Visão Cidades')

#Primeiro container com um gráfico
with st.container():
    fig = bar_1(df)
    st.plotly_chart(fig,use_container_width=True,theme=None)
    
    
#Segundo container com um gráfico
with st.container():
    fig = bar_2(df)
    st.plotly_chart(fig,use_container_width=True,theme=None)
    
    
#Terceiro container com um gráfico            
with st.container():
    fig = bar_3(df)
    st.plotly_chart(fig,use_container_width=True,theme=None)
        
        
#Terceiro container com um gráfico
with st.container():
    fig = bar_4(df)
    st.plotly_chart(fig,use_container_width=True,theme=None)


