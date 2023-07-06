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
st.set_page_config(page_title="Cities", page_icon=":cityscape:", layout="wide")


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


## Outras funções utilizadas:


# Função Cidades com Mais Restaurantes:
def top_ten_cities_restaurants(countries_options):
    """Esta função seleciona os dados dos países escolhidos e cria um gráfico de barras
    mostrando as dez cidades com mais restaurantes na base de dados.

    Etapas:
    1 - Filtrar os dados do DataFrame com base nos países selecionados.
    2 - Selecionar as colunas "Restaurant_ID", "Country_Name" e "City".
    3 - Agrupar os dados por país e cidade.
    4 - Contar a quantidade de restaurantes em cada cidade.
    5 - Ordenar os resultados pela quantidade de restaurantes em ordem decrescente.
    6 - Resetar o índice do DataFrame resultante.
    7 - Criar um gráfico de barras com as dez primeiras cidades com mais restaurantes.
    8 - Definir a coluna "City" como eixo x, a coluna "Restaurant_ID" como eixo y e a coluna "Country_Name" como cor das barras.
    9 - Adicionar rótulos nos valores das barras com duas casas decimais.
    10- Adicionar labels personalizados para os eixos e a cor das barras.
    11- Adicionar um título ao gráfico.
    12- Retornar o gráfico resultante.

    Input: Dados dos países, cidades e restaurantes para análise.
    Output: Gráfico de barras com as top 10 cidades com mais restaurantes.
    """
    # Selecionar os dados no Dataframe:
    df_cidades_mais_restaurantes = (
        df.loc[
            df["Country_Name"].isin(countries_options),
            ["Restaurant_ID", "Country_Name", "City"],
        ]
        .groupby(["Country_Name", "City"])
        .count()
        .sort_values(["Restaurant_ID"], ascending=False)
        .reset_index()
    )
    # Desenhar o Gráfico de Linhas:
    fig = px.bar(
        df_cidades_mais_restaurantes.head(10),
        x="City",
        y="Restaurant_ID",
        text="Restaurant_ID",
        text_auto=".2f",
        color="Country_Name",
        labels={
            "City": "Cidade",
            "Restaurant_ID": "Quantidade de Restaurantes",
            "Country_Name": "País",
        },
    )

    fig.update_layout(
        title="Top 10 Cidades com mais Restaurantes na Base de Dados", title_x=0.25
    )

    return fig


# Função Top 7 Melhores Restaurantes:
def best_seven_restaurants(countries_options):
    """Esta função seleciona os dados dos países escolhidos e cria um gráfico de barras mostrando as sete cidades
    com as maiores médias de avaliação (nota 4 ou superior) entre os restaurantes.

    Etapas:
    1 - Selecionar os restaurantes com avaliação igual ou superior a 4.
    2 - Filtrar os dados dos países selecionados.
    3 - Agrupar os dados por país e cidade e contar o número de restaurantes em cada cidade.
    4 - Desenhar um gráfico de barras com as cidades e a quantidade de restaurantes.
    5 - Personalizar o layout do gráfico, incluindo título e rótulos.
    6 - Retornar o gráfico resultante.

    Input: Dados dos países, cidades e restaurantes para análise.
    Output: Gráfico de barras com as top 7 cidades com mais restaurantes com média de avaliação superior a 4.
    """
    # Selecionar os dados no Dataframe:
    cidades_mais_restaurantes_nota4 = df.loc[
        (df["Aggregate_rating"] >= 4), ["City", "Country_Name", "Aggregate_rating"]
    ]
    df_cidades_mais_restaurantes_nota4 = (
        cidades_mais_restaurantes_nota4.loc[
            cidades_mais_restaurantes_nota4["Country_Name"].isin(countries_options),
            ["City", "Country_Name", "Aggregate_rating"],
        ]
        .groupby(["Country_Name", "City"])
        .count()
        .sort_values(["Aggregate_rating"], ascending=False)
        .reset_index()
    )

    # Desenhar o Gráfico de Linhas:
    fig = px.bar(
        df_cidades_mais_restaurantes_nota4.head(7),
        x="City",
        y="Aggregate_rating",
        text="Aggregate_rating",
        text_auto=".2f",
        color="Country_Name",
        labels={
            "City": "Cidade",
            "Aggregate_rating": "Quantidade de Restaurantes",
            "Country_Name": "País",
        },
    )

    fig.update_layout(
        title="Top 7 Cidades com média alta(>4) de avaliação", title_x=0.15
    )

    return fig


# Função Top 7 Piores Restaurantes:
def worst_seven_restaurants(countries_options):
    """Esta função seleciona os dados dos países escolhidos e cria um gráfico de barras mostrando as sete cidades
    com as piores média de avaliação (nota 2.5 ou inferior) entre os restaurantes.

    Etapas:
    1 - Selecionar os restaurantes com avaliação igual ou inferior a 2.5.
    2 - Filtrar os dados dos países selecionados.
    3 - Agrupar os dados por país e cidade e contar o número de restaurantes em cada cidade.
    4 - Desenhar um gráfico de barras com as cidades e a quantidade de restaurantes.
    5 - Personalizar o layout do gráfico, incluindo título e rótulos.
    6 - Retornar o gráfico resultante.

    Input: Dados dos países, cidades e restaurantes para análise.
    Output: Gráfico de barras com as top 7 cidades com mais restaurantes com média de avaliação inferior a 2.5.
    """
    # Selecionar os dados no Dataframe:
    cidades_mais_restaurantes_nota25 = df.loc[
        (df["Aggregate_rating"] <= 2.5), ["City", "Country_Name", "Aggregate_rating"]
    ]
    df_cidades_mais_restaurantes_nota25 = (
        cidades_mais_restaurantes_nota25.loc[
            cidades_mais_restaurantes_nota25["Country_Name"].isin(countries_options),
            ["City", "Country_Name", "Aggregate_rating"],
        ]
        .groupby(["Country_Name", "City"])
        .count()
        .sort_values(["Aggregate_rating"], ascending=False)
        .reset_index()
    )

    # Desenhar o Gráfico de Linhas:
    fig = px.bar(
        df_cidades_mais_restaurantes_nota25.head(7),
        x="City",
        y="Aggregate_rating",
        text="Aggregate_rating",
        text_auto=".2f",
        color="Country_Name",
        labels={
            "City": "Cidade",
            "Aggregate_rating": "Quantidade de Restaurantes",
            "Country_Name": "País",
        },
    )

    fig.update_layout(
        title="Top 7 Cidades com média baixa(<2.5) de avaliação", title_x=0.15
    )

    return fig


# Função Top 10 Cidades com mais Restaurantes de Culinárias distintas:


def top_ten_cities_unique_cuisines(countries_options):
    """Esta função seleciona os dados das cidades com o maior número de tipos únicos de culinária em países específicos.
    Em seguida, cria um gráfico de barras mostrando as 10 principais cidades e a quantidade de restaurantes com culinárias únicas.

    Etapas:
    1 - Selecionar os dados das colunas "Country_Name", "City" e "Cuisines" no DataFrame.
    2 - Filtrar os dados dos países selecionados.
    3 - Agrupar os dados por país e cidade e contar o número de tipos únicos de culinária em cada cidade.
    4 - Ordenar os dados em ordem decrescente com base na quantidade de tipos únicos de culinária.
    5 - Resetar o índice dos dados.
    6 - Desenhar um gráfico de barras com as cidades e a quantidade de restaurantes com tipos únicos de culinária.
    7 - Personalizar o layout do gráfico, incluindo título e rótulos.
    8 - Retornar o gráfico resultante.

    Input: Dados dos países, cidades, restaurantes e tipos de culinária para análise.
    Output: Gráfico de barras com as top 10 cidades com mais restaurantes de tipo de culinária única.
    """
    # Selecionar os dados no Dataframe:
    cidades_maior_tipos_culinaria = (
        df.loc[
            df["Country_Name"].isin(countries_options),
            ["Country_Name", "City", "Cuisines"],
        ]
        .groupby(["Country_Name", "City"])
        .nunique()
        .sort_values(["Cuisines"], ascending=False)
        .reset_index()
    )

    # Desenhar o Gráfico de Linhas:
    fig = px.bar(
        cidades_maior_tipos_culinaria.head(10),
        x="City",
        y="Cuisines",
        text="Cuisines",
        color="Country_Name",
        labels={
            "City": "Cidade",
            "Cuisines": "Quantidade de Restaurantes com Culinárias Únicas",
            "Country_Name": "País",
        },
    )

    fig.update_layout(
        title="Top 10 Cidades com mais Restaurantes com Tipos Únicos de Culinária",
        title_x=0.20,
    )

    return fig


# --------------------------------------------- Início da Estrutura Lógica do Código ---------------------------------------------------------

# Header da Página:
st.title(":cityscape: Visão Cidades")

# Sidebar:
image = Image.open("logo.png")
st.sidebar.image(image, width=120)

st.sidebar.markdown("# Fome Zero")

# Função Filtros da Página:

st.sidebar.markdown("## Filtros")
st.sidebar.markdown("#### Escolha os países para visualizar os dados dos restaurantes:")


def create_filter_countries(df):
    countries_options = st.sidebar.multiselect(
        "Quais países?",
        df.loc[:, "Country_Name"].unique().tolist(),
        default=[
            "Australia",
            "Brazil",
            "Canada",
            "England",
            "India",
            "Qatar",
            "South Africa",
            "United States of America",
        ],
    )

    return list(countries_options)


# Ativar o Filtro nos Gráficos:
countries_options = create_filter_countries(df)


###############################################
# Layout no Streamlit:
###############################################

with st.container():
    # Quantidade de Restaurantes por cidades:
    fig = top_ten_cities_restaurants(countries_options)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""___""")


with st.container():
    # Melhores e Piores Restaurantes avaliados na Plataforma:
    best, worst = st.columns(2, gap="large")
    with best:
        # Top 7 Melhores:
        fig = best_seven_restaurants(countries_options)
        st.plotly_chart(fig, use_container_width=True)
    with worst:
        # Top 7 Piores:
        fig = worst_seven_restaurants(countries_options)
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown("""___""")
    # Top 10 Cidades com mais Restaurantes de Culinárias distintas:
    fig = top_ten_cities_unique_cuisines(countries_options)
    st.plotly_chart(fig, use_container_width=True)
