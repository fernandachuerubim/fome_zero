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
    page_title='Main Page',page_icon='📊', layout='wide',initial_sidebar_state="expanded")


#===================================================================================================================
#Funções
#===================================================================================================================


def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

def apply_func(df):
    df['Price range'] = df.loc[:, 'Price range'].apply(lambda x: create_price_tye(x))
    df['Cuisines'] = df['Cuisines'].astype(str)
    df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])
    return df


def clean_code(df):
    df = df.loc[(df['Cuisines'] != 'nan'),:].copy()
    df = df.loc[(df['Cuisines'] != 'Drinks Only'),:].copy()
    df = df.loc[(df['Cuisines'] != 'Mineira'),:].copy()
    df = df.drop_duplicates().reset_index(drop=True)
    return df

def ajuste_votes(df):
    re1 = df['Votes'].sum()
    re1 = f'{re1:,.0f}'
    re1 = re1.replace(',','.')
    return re1

def restaurantes_map(df):
    re6 = df.loc[:,['Restaurant Name','Average Cost for two','Currency','Aggregate rating','country','City','Cuisines','Latitude','Longitude']]
    map = folium.Map(location=[0, 0],zoom_start=2)
    marker_cluster = folium.plugins.MarkerCluster().add_to(map)
    for index,location in re6.iterrows():
        folium.Marker([location['Latitude'],location['Longitude']],
                    popup=folium.Popup(f'''<h6><b>{location['Restaurant Name']}</b></h6>
                    <h6>Preço: {location['Average Cost for two']} ({location['Currency']}) para dois <br>
                    Culinária: {location['Cuisines']} <br>
                    Avaliação: {location['Aggregate rating']}/5.0</h6>''',
                    max_width=300,min_width=150),
                    tooltip=location["Restaurant Name"],
                    icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(marker_cluster)

    folium_static(map,width=1024,height=600)
    ### Lembrar de definir os agrupamentos dos países


#=============================Inicio da Estrutura Lógica do Código=====================================================
#================
#import dataset
#================
df = pd.read_csv(r'df_country.csv')


# ===========================================================================
#Limpando os dados
#==========================================================================
df1 = df.copy()
df1 = apply_func(df1)
df1 = clean_code(df1)
df2 = df1.copy()


#===================================================================================================================
#Barra lateral
#===================================================================================================================

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Filtros')

country = ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey']
country_op = st.sidebar.multiselect('Escolha os Países que Deseja visualizar as informações',
                      country,
                      default=['Brazil','England','Qatar', 'South Africa','Canada','Australia'])

df1 = df1.loc[df1['country'].isin(country_op),:]




#===================================================================================================================
#Layout no Streamlit
#===================================================================================================================
st.markdown('# Fome Zero!')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')

#Primeiro container dividido em 5 colunas
with st.container():
    st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        re1 = len(df2['Restaurant ID'].unique())
        col1.metric('Restaurantes Cadastrados',re1)
        
    with col2:
        re1 = len(df2['country'].unique())
        col2.metric('Países Cadastrados',re1)
        
    with col3:
        re1 = len(df2['City'].unique())
        col3.metric('Cidades Cadastrados',re1)
        
    with col4:       
        re1 = ajuste_votes(df)
        col4.metric('Avaliações Feitas na Plataforma',re1)
        
    with col5:
        re1 = len(df2['Cuisines'].unique())
        col5.metric('Tipos de Culinárias Oferecidas',re1)
    
    
#Segundo container com o mapa
with st.container():
    restaurantes_map(df1)
    