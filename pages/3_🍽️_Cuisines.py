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
    page_title='Cuisines', page_icon='🍽️', layout='wide')


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


def max_rating_cuisines(df,tipo):
    re1 = df.loc[(df['Cuisines'] == tipo),['Restaurant Name','Restaurant ID','Aggregate rating']].groupby(['Restaurant Name','Restaurant ID']).mean().sort_values(by='Aggregate rating',ascending=False).reset_index()
    re1 = re1.loc[re1['Aggregate rating'] == re1['Aggregate rating'].max(),['Restaurant Name','Restaurant ID']].groupby('Restaurant Name').min().sort_values(by='Restaurant ID',ascending=True).reset_index()

    re1 = df.loc[df['Restaurant ID'] == re1.iloc[0,1],['Restaurant Name','country','City','Average Cost for two','Currency','Cuisines','Aggregate rating']]
    
    label = f'{re1.iloc[0,5]}: {re1.iloc[0,0]}'
    value = f'{re1.iloc[0,6]}/5.0'
    ajuda = f'''País: {re1.iloc[0,1]}
        
Cidade: {re1.iloc[0,2]}
        
Média Prato para dois: {re1.iloc[0,3]} {re1.iloc[0,4]}'''
    
    return label,value,ajuda


def top_dataframe(df1):
    dataframe = df1.loc[df1['Aggregate rating'] == df1['Aggregate rating'].max(),['Restaurant ID', 'Restaurant Name', 'country', 'City','Cuisines','Average Cost for two','Aggregate rating','Votes']].sort_values(by='Restaurant ID',ascending=True)
    dataframe['Restaurant ID'] = df1.loc[:, 'Restaurant ID'].apply(lambda x: "{0:>20}".format(x))
    dataframe['Votes'] = df1.loc[:, 'Votes'].apply(lambda x: "{0:>20}".format(x))
    dataframe.columns = ['ID Restaurante', 'Nome do Restaurante', 'País', 'Cidade','Culinária','Média do preço de um prato para dois','Avaliação média','Qtde de votos']
    return dataframe


def bar_1(df1,data_slider):
    graf1 = round(df3.loc[:,['Cuisines','Aggregate rating']].groupby(['Cuisines']).mean().sort_values(by='Aggregate rating',ascending=False).reset_index(),2)
    graf1 = px.bar(graf1.head(data_slider), x='Cuisines',y='Aggregate rating',text_auto=True,labels={'Cuisines':'Tipo de Culinária','Aggregate rating':'Média da Avaliação Média'},title=f'Top {data_slider} Melhores Tipos de Culinárias')
    return graf1
        
        
def bar_2(df1,data_slider):
    graf1 = round(df3.loc[:,['Cuisines','Aggregate rating']].groupby(['Cuisines']).mean().sort_values(by='Aggregate rating',ascending=True).reset_index(),2)
    graf1 = px.bar(graf1.head(data_slider), x='Cuisines',y='Aggregate rating',text_auto=True,labels={'Cuisines':'Tipo de Culinária','Aggregate rating':'Média da Avaliação Média'},title=f'Top {data_slider} Piores Tipos de Culinárias')
    return graf1


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
df3 = df1.copy()


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

df1 = df1.loc[df1['country'].isin(country_op),:]
df3 = df3.loc[df3['country'].isin(country_op),:]


data_slider = st.sidebar.slider('Selecione a quantidade de Restaurantes que deseja visualizar',
                 value=10,
                 min_value=1,
                 max_value=20)


cuisines_list = ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian', 'Author',
       'Gourmet Fast Food', 'Lebanese', 'Modern Australian', 'African',
       'Coffee and Tea', 'Australian', 'Middle Eastern', 'Malaysian',
       'Tapas', 'New American', 'Pub Food', 'Southern', 'Diner', 'Donuts',
       'Southwestern', 'Sandwich', 'Irish', 'Mediterranean', 'Cafe Food',
       'Korean BBQ', 'Fusion', 'Canadian', 'Breakfast', 'Cajun',
       'New Mexican', 'Belgian', 'Cuban', 'Taco', 'Caribbean', 'Polish',
       'Deli', 'British', 'California', 'Others', 'Eastern European',
       'Creole', 'Ramen', 'Ukrainian', 'Hawaiian', 'Patisserie',
       'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan', 'Burmese',
       'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian', 'Continental',
       'South Indian', 'North Indian', 'Salad', 'Finger Food', 'Mandi',
       'Turkish', 'Kerala', 'Pakistani', 'Biryani', 'Street Food',
       'Nepalese', 'Goan', 'Iranian', 'Mughlai', 'Rajasthani', 'Mithai',
       'Maharashtrian', 'Gujarati', 'Rolls', 'Momos', 'Parsi',
       'Modern Indian', 'Andhra', 'Tibetan', 'Kebab', 'Chettinad',
       'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi', 'Afghan',
       'Lucknowi', 'Charcoal Chicken', 'Mangalorean', 'Egyptian',
       'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian', 'Western',
       'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian', 'Balti',
       'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji', 'South African',
       'Durban', 'World Cuisine', 'Izgara', 'Home-made', 'Giblets',
       'Fresh Fish', 'Restaurant Cafe', 'Kumpir', 'Döner',
       'Turkish Pizza', 'Ottoman', 'Old Turkish Bars', 'Kokoreç']
cuisines_op = st.sidebar.multiselect('Escolha os Tipos de Culinária',
                      cuisines_list,
                      default=['Home-made','BBQ','Japanese', 'Brazilian','Arabian','American','Italian'])
df1 = df1.loc[df1['Cuisines'].isin(cuisines_op),:]


st.sidebar.markdown ( """---""" )
st.sidebar.markdown( '### Powered by Comunidade DS' )



#===================================================================================================================
#Layout no Streamlit
#===================================================================================================================

st.markdown('# 🍽️ Visão Tipos de Culinárias')
st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')


#Primeiro container dividio em 5 colunas
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        label, value, ajuda = max_rating_cuisines(df2,'Italian')
        col1.metric(label,value,help=ajuda)
               
    with col2:
        label, value, ajuda = max_rating_cuisines(df2,'American')
        col2.metric(label,value,help=ajuda)
        
    with col3:
        label, value, ajuda = max_rating_cuisines(df2,'Arabian')
        col3.metric(label,value,help=ajuda)
        
    with col4:       
        label, value, ajuda = max_rating_cuisines(df2,'Japanese')
        col4.metric(label,value,help=ajuda)
        
    with col5:
        label, value, ajuda = max_rating_cuisines(df2,'Brazilian')
        col5.metric(label,value,help=ajuda)
    
    
#Segundo container com o DataFrame
with st.container():
    st.markdown(f'## Top {data_slider} Restaurantes')
    dataframe = top_dataframe(df1)
    st.dataframe(dataframe.head(data_slider))
    

#Terceiro container com duas colunas, cada qual com um gráfico
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        graf1 = bar_1(df1,data_slider)
        st.plotly_chart(graf1,use_container_width=True,theme=None)
        
    with col2:
        graf1 = bar_2(df1,data_slider)
        st.plotly_chart(graf1,use_container_width=True,theme=None)

