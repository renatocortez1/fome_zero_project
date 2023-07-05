# Importando as Bibliotecas:

import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

# --------------------------------------
# Importando o data set:
df_raw = pd.read_csv("zomato.csv")
df = df_raw.copy()

# Configurando a apresentação da Página:
st.set_page_config(
    page_title="Cuisines",
    page_icon=":knife_fork_plate:",
    layout="wide",
)


# --------------------------------------------------------------------------------------------------
#                                           Funções
# --------------------------------------------------------------------------------------------------


# Função de Limpeza do Conjunto de Dados:
def clean_code(df):
    """Esta função tem a responsabilidade de limpar o dataframe

    Tipos de Limpeza:
    1. Remoção da coluna de valores vazios 'Swith to order menu'
    2. Renomeia as colunas do Dataframe
    3. Remoção de dados duplicados
    4. Remoção os valores NA que forem np.na
    5. Categorização de todos os restaurantes  por somente um tipo de culinária
    6. Retirada de registros com Média Negativa de Avaliação

    Input: Dataframe Sujo
    Output: Dataframe Limpo
    """

    # 1. Retirar a coluna de valores vazios 'Swith to order menu':
    df = df.drop("Switch to order menu", axis=1)

    # 2. Renomeando as colunas do Dataframe:
    df = df.rename(
        columns={
            "Restaurant ID": "Restaurant_ID",
            "Restaurant Name": "Restaurant_Name",
            "Country Code": "Country_Name",
            "Locality Verbose": "Locality_Verbose",
            "Average Cost for two": "Average_Cost_for_two",
            "Has Table booking": "Has_Table_booking",
            "Has Online delivery": "Has_Online_delivery",
            "Is delivering now": "Is_delivering_now",
            "Price range": "Price_range",
            "Aggregate rating": "Aggregate_rating",
            "Rating color": "Rating_color",
            "Rating text": "Rating_text",
        }
    )

    # 3. Remove Dados Duplicados:
    df_sem_duplicatas = df.drop_duplicates()
    df = df_sem_duplicatas

    # 4. Remove os NA que forem np.na:
    df = df.dropna()

    # 5. Categorizar todos os restaurantes somente por um tipo de culinária:
    df["Cuisines"] = df.loc[:, "Cuisines"].astype(str).apply(lambda x: x.split(",")[0])

    # 6. Retirar Registros com Média Negativa de Avaliação:
    linhas_negativas = df["Cuisines"] != "Mineira"
    df = df.loc[linhas_negativas, :]
    linhas_negativas2 = df["Cuisines"] != "Drinks Only"
    df = df.loc[linhas_negativas2, :]

    return df


# Limpando os Dados chamando a função clean_code:
df = clean_code(df)

# -----------------------------------------------------------------------------------------
# Funções Fornecidas previamente
# -----------------------------------------------------------------------------------------

# Função para colocar o nome dos países com base no código de cada país:
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}


def country_name(Country_ID):
    return COUNTRIES[Country_ID]


df["Country_Name"] = df["Country_Name"].map(country_name)

# Função para criação do nome das Cores:
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}


def color_name(color_code):
    return COLORS[color_code]


df["Rating_color"] = df["Rating_color"].map(color_name)


# Função para Criação do Tipo de Categoria de Comida
def create_price_type(Price_range):
    if Price_range == 1:
        return "cheap"
    elif Price_range == 2:
        return "normal"
    elif Price_range == 3:
        return "expensive"
    else:
        return "gourmet"


df["Price_range"] = df["Price_range"].map(create_price_type)

## -------------------------------------------------- Outras funções utilizadas: --------------------------------------------------------


# Função Melhores Restaurantes dos Tipos de Culinária principais:
def get_best_restaurant(cuisine):
    """Esta função seleciona os melhores restaurantes de uma determinada culinária, com base em sua avaliação e número de votos,
    e retorna o tipo de culinária, o nome e a avaliação do restaurante com a melhor classificação.

    Etapas:
    1 - Selecionar os dados dos restaurantes que possuem uma determinada culinária.
    2 - Ordenar os restaurantes selecionados pelo rating agregado e pelo número de votos, em ordem descendente.
    3 - Selecionar os cinco melhores restaurantes.
    4 - Resetar o índice dos restaurantes selecionados.
    5 - Extrair o tipo de culinária, o nome do restaurante e a avaliação do restaurante com a melhor classificação dos dados selecionados.
    6 - Retornar o tipo de culinária, o nome do restaurante e a avaliação do restaurante com a melhor classificação.

    Input: Dados dos países, cidades, restaurantes e tipos de culinária para análise.
    Output: Nomes dos melhores restaurantes, a culinária e suas avaliações.
    """
    restaurantes = df.loc[
        df["Cuisines"] == cuisine,
        ["Country_Name", "Restaurant_Name", "Cuisines", "Aggregate_rating", "Votes"],
    ]
    maiores_restaurantes = (
        restaurantes.sort_values(["Aggregate_rating", "Votes"], ascending=False)
        .head()
        .reset_index()
    )

    tipo_culinaria = maiores_restaurantes["Cuisines"].values[0]
    nome_maior = maiores_restaurantes["Restaurant_Name"].values[0]
    avaliacao_maior = maiores_restaurantes["Aggregate_rating"].values[0]
    return tipo_culinaria, nome_maior, avaliacao_maior


# Função Top 20 Melhores Restaurantes entre os Países e Culinárias Selecionadas
def top_twenty_best_restaurants(df):
    """Esta função seleciona os 20 melhores restaurantes com base na maior média de avaliação entre aqueles que têm pelo menos 150 votos.
    Ela retorna um dataframe com o nome do restaurante, o país, as culinárias oferecidas, a avaliação agregada e o número de votos.

    Etapas:
    1 - Selecionar os restaurantes com pelo menos 150 votos no dataframe.
    2 - Agrupar os restaurantes pelo nome.
    3 - Para cada grupo de restaurantes, selecionar o registro com a maior avaliação agregada e o maior número de votos.
    4 - Classificar os restaurantes com base na avaliação agregada e no número de votos em ordem decrescente.
    5 - Selecionar os 20 melhores restaurantes.
    6 - Resetar o índice do dataframe resultante.
    7 - Retornar o dataframe com os 20 melhores restaurantes.

    Input: Dados dos países, cidades, restaurantes e tipos de culinária para análise.
    Output: Tabela com os 20 melhores restaurantes nas condições propostas.
    """
    restaurante_maior_nota_media = (
        df.loc[
            (df["Votes"] >= 150),
            [
                "Restaurant_Name",
                "Country_Name",
                "Cuisines",
                "Aggregate_rating",
                "Votes",
            ],
        ]
        .groupby("Restaurant_Name")
        .max()
        .sort_values(["Aggregate_rating", "Votes"], ascending=False)
        .head(20)
        .reset_index()
    )
    return restaurante_maior_nota_media


# Função Top 10 Melhores/Piores Tipos de Culinária:


def top_types_cuisines(df, top_asc):
    """Esta função seleciona os dados de tipos de culinária com pelo menos 100 votos, calcula a média de avaliação agregada para
    cada tipo de culinária, classifica os tipos de culinária com base na média em ordem ascendente ou descendente e
    retorna um gráfico de barras dos 10 melhores ou piores tipos de culinária.

    Etapas:
    1 - Selecionar os dados no dataframe, considerando apenas os registros com pelo menos 100 votos.
    2 - Agrupar os dados pela coluna "Cuisines".
    3 - Calcular a média da avaliação agregada para cada tipo de culinária.
    4 - Classificar os tipos de culinária com base na média da avaliação agregada, em ordem ascendente ou descendente, dependendo do parâmetro "top_asc".
    5 - Resetar o índice do dataframe resultante.
    6 - Desenhar um gráfico de barras com os 10 melhores ou piores tipos de culinária, dependendo do parâmetro "top_asc".
    7 - Configurar as legendas e rótulos do gráfico.
    8 - Retornar o gráfico.

    Input: Dados dos países, cidades, restaurantes e tipos de culinária para análise.
    Output: Gráfico de barras dos 10 melhores ou piores tipos de culinária nos países selecionados.
    """
    # Selecionando os dados no Dataframe:
    culinaria_media = round(
        df.loc[
            (df["Votes"] >= 100),
            [
                "Cuisines",
                "Aggregate_rating",
            ],
        ]
        .groupby("Cuisines")
        .mean()
        .sort_values(["Aggregate_rating"], ascending=top_asc)
        .reset_index(),
        2,
    )

    # Desenhar o Gráfico de Linhas:
    fig = px.bar(
        culinaria_media.head(10),
        x="Cuisines",
        y="Aggregate_rating",
        text="Aggregate_rating",
        labels={
            "Cuisines": "Tipo de Culinária",
            "Aggregate_rating": "Média de Avaliações",
        },
    )
    return fig


# --------------------------------------------- Início da Estrutura Lógica do Código ---------------------------------------------------------

# Header da Página:
st.title(":knife_fork_plate: Visão Cozinhas")

# Sidebar:
image = Image.open("logo.png")
st.sidebar.image(image, width=120)

st.sidebar.markdown("# Fome Zero")

# Filtros da Página:
st.sidebar.markdown("## Filtros")
# Filtro de País:
st.sidebar.markdown("#### Escolha os países para visualizar os dados dos restaurantes:")
countries_options = st.sidebar.multiselect(
    "Quais países?",
    [
        "Australia",
        "Brazil",
        "Canada",
        "England",
        "India",
        "Indonesia",
        "New Zeland",
        "Philippines",
        "Qatar",
        "Singapure",
        "South Africa",
        "Sri Lanka",
        "Turkey",
        "United Arab Emirates",
        "United States of America",
    ],
    default=[
        "Australia",
        "Brazil",
        "Canada",
        "England",
        "India",
        "United States of America",
    ],
)

# Filtro dos Tipos de Culinária:
st.sidebar.markdown("#### Escolha os Tipos de Culinária:")
cuisines_types = st.sidebar.multiselect(
    "Quais culinárias?",
    [
        "Italian",
        "European",
        "Filipino",
        "American",
        "Korean",
        "Pizza",
        "Taiwanese",
        "Japanese",
        "Coffee",
        "Chinese",
        "Seafood",
        "Singaporean",
        "Vietnamese",
        "Latin American",
        "Healthy Food",
        "Cafe",
        "Fast Food",
        "Brazilian",
        "Argentine",
        "Arabian",
        "Bakery",
        "Tex-Mex",
        "Bar Food",
        "International",
        "French",
        "Steak",
        "German",
        "Sushi",
        "Grill",
        "Peruvian",
        "North Eastern",
        "Ice Cream",
        "Burger",
        "Mexican",
        "Vegetarian",
        "Contemporary",
        "Desserts",
        "Juices",
        "Beverages",
        "Spanish",
        "Thai",
        "Indian",
        "BBQ",
        "Mongolian",
        "Portuguese",
        "Greek",
        "Asian",
        "Author",
        "Gourmet Fast Food",
        "Lebanese",
        "Modern Australian",
        "African",
        "Coffee and Tea",
        "Australian",
        "Middle Eastern",
        "Malaysian",
        "Tapas",
        "New American",
        "Pub Food",
        "Southern",
        "Diner",
        "Donuts",
        "Southwestern",
        "Sandwich",
        "Irish",
        "Mediterranean",
        "Cafe Food",
        "Korean BBQ",
        "Fusion",
        "Canadian",
        "Breakfast",
        "Cajun",
        "New Mexican",
        "Belgian",
        "Cuban",
        "Taco",
        "Caribbean",
        "Polish",
        "Deli",
        "British",
        "California",
        "Others",
        "Eastern European",
        "Creole",
        "Ramen",
        "Ukrainian",
        "Hawaiian",
        "Patisserie",
        "Yum Cha",
        "Pacific Northwest",
        "Tea",
        "Moroccan",
        "Burmese",
        "Dim Sum",
        "Crepes",
        "Fish and Chips",
        "Russian",
        "Continental",
        "South Indian",
        "North Indian",
        "Salad",
        "Finger Food",
        "Mandi",
        "Turkish",
        "Kerala",
        "Pakistani",
        "Biryani",
        "Street Food",
        "Nepalese",
        "Goan",
        "Iranian",
        "Mughlai",
        "Rajasthani",
        "Mithai",
        "Maharashtrian",
        "Gujarati",
        "Rolls",
        "Momos",
        "Parsi",
        "Modern Indian",
        "Andhra",
        "Tibetan",
        "Kebab",
        "Chettinad",
        "Bengali",
        "Assamese",
        "Naga",
        "Hyderabadi",
        "Awadhi",
        "Afghan",
        "Lucknowi",
        "Charcoal Chicken",
        "Mangalorean",
        "Egyptian",
        "Malwani",
        "Armenian",
        "Roast Chicken",
        "Indonesian",
        "Western",
        "Dimsum",
        "Sunda",
        "Kiwi",
        "Asian Fusion",
        "Pan Asian",
        "Balti",
        "Scottish",
        "Cantonese",
        "Sri Lankan",
        "Khaleeji",
        "South African",
        "Durban",
        "World Cuisine",
        "Izgara",
        "Home-made",
        "Giblets",
        "Fresh Fish",
        "Restaurant Cafe",
        "Kumpir",
        "Döner",
        "Turkish Pizza",
        "Ottoman",
        "Old Turkish Bars",
        "Kokoreç",
    ],
    default=[
        "Japanese",
        "Brazilian",
        "Arabian",
        "American",
        "Italian",
        "BBQ",
        "Caribbean",
        "Seafood",
        "Australian",
        "Mediterranean",
        "Vegetarian",
        "Pizza",
        "Cuban",
        "Greek",
        "Mongolian",
    ],
)

# Ativar o Filtro nos Gráficos:

# Filtro de Países:
linhas_selecionadas = df["Country_Name"].isin(countries_options)
df = df.loc[linhas_selecionadas, :]

# Filtro dos Tipos de Culinária:
linhas_selecionadas = df["Cuisines"].isin(cuisines_types)
df = df.loc[linhas_selecionadas, :]


# --------------------------------------------- Layout do Streamlit ---------------------------------------------------------

# Container de Dados sobre os principais tipos culinários:
st.subheader("Melhores Restaurantes das Principais Culinárias nos Países Selecionados:")
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5, gap="large")
    with col1:
        tipo_culinaria, nome_maior, avaliacao_maior = get_best_restaurant("Italian")
        col1.metric(
            f"{tipo_culinaria}: {nome_maior}",
            f"{avaliacao_maior}/5.0",
        )
    with col2:
        tipo_culinaria, nome_maior, avaliacao_maior = get_best_restaurant("American")
        col2.metric(
            f"{tipo_culinaria}: {nome_maior}",
            f"{avaliacao_maior}/5.0",
        )
    with col3:
        tipo_culinaria, nome_maior, avaliacao_maior = get_best_restaurant("Arabian")
        col3.metric(
            f"{tipo_culinaria}: {nome_maior}",
            f"{avaliacao_maior}/5.0",
        )
    with col4:
        tipo_culinaria, nome_maior, avaliacao_maior = get_best_restaurant("Japanese")
        col4.metric(
            f"{tipo_culinaria}: {nome_maior}",
            f"{avaliacao_maior}/5.0",
        )
    with col5:
        tipo_culinaria, nome_maior, avaliacao_maior = get_best_restaurant("Brazilian")
        col5.metric(
            f"{tipo_culinaria}: {nome_maior}",
            f"{avaliacao_maior}/5.0",
        )

with st.container():
    st.markdown("""___""")
    st.subheader(
        "Top 20 Melhores Restaurantes entre os Países e Culinárias Selecionadas"
    )
    restaurante_maior_nota_media = top_twenty_best_restaurants(df)
    st.dataframe(restaurante_maior_nota_media)

with st.container():
    st.markdown("""___""")
    best, worst = st.columns(2, gap="large")
    with best:
        st.markdown(
            "<div style='text-align: center'><h4>Top 10 Melhores Tipos de Culinárias</h4></div>",
            unsafe_allow_html=True,
        )
        fig = top_types_cuisines(df, top_asc=False)
        st.plotly_chart(fig, use_container_width=True)
    with worst:
        st.markdown(
            "<div style='text-align: center'><h4>Top 10 Piores Tipos de Culinárias</h4></div>",
            unsafe_allow_html=True,
        )
        fig = top_types_cuisines(df, top_asc=True)
        st.plotly_chart(fig, use_container_width=True)
