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
st.set_page_config(page_title="Countries", page_icon=":earth_americas:", layout="wide")


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

# _____________________________________________________________________

# Outras funções utilizadas:


# Função da quantidade de restaurantes por cidades:
def restaurants_by_countries(countries_options):
    """Esta função cria um gráfico da quantidade de restaurantes registrados por país.

    Assim, calcula quantos restaurantes por país existentes no DataFrame. Ela realiza as seguintes etapas:
    1 - Seleciona as colunas relevantes do DataFrame, que são o nome do país e o ID do restaurante.
    2 - Agrupa os dados pelo nome do país e conta quantos restaurantes existem em cada país.
    3 - Classifica os resultados em ordem decrescente com base na quantidade de restaurantes.
    4 - Renomeia as colunas para "Países" e "Quantidade de Restaurantes".
    5 - Cria um gráfico de barras usando a biblioteca Plotly Express, onde os países são exibidos no eixo x e a quantidade de restaurantes no eixo y.
    6 - Adiciona um título ao gráfico.
    7 - Adiciona os valores da quantidade de restaurantes dentro das barras do gráfico.
    8 - Retorna o gráfico resultante.


    Input: Dados da quantidade de restaurantes por país.
    Output: Gráfico de barras com os valores encontrados.
    """

    cols = ["Country_Name", "Restaurant_ID"]
    # Seleção de Linhas
    df_aux = (
        df.loc[df["Country_Name"].isin(countries_options), cols]
        .groupby("Country_Name")
        .count()
        .sort_values(["Restaurant_ID"], ascending=False)
        .reset_index()
    )

    # Alterar os nomes das colunas
    df_aux = df_aux.rename(
        columns={
            "Country_Name": "Países",
            "Restaurant_ID": "Quantidade de Restaurantes",
        }
    )

    # Desenhar o Gráfico de Linhas
    fig = px.bar(df_aux, x="Países", y="Quantidade de Restaurantes")

    # Adicionar um título ao gráfico
    fig.update_layout(
        title="Quantidade de Restaurantes Registrados por País", title_x=0.33
    )

    #  Adicionar os valores dentro das barras
    fig.update_traces(text=df_aux["Quantidade de Restaurantes"], textposition="auto")

    return fig


# Função da quantidade de cidades por país:


def cities_by_countries(countries_options):
    """Essa função calcula e exibe um gráfico de barras mostrando a quantidade de cidades registradas por país..

    Assim, calcula quantos restaurantes por cidades que existem no DataFrame. Ela realiza as seguintes etapas:
    1 - Selecionar as colunas relevantes do DataFrame: "Country_Name" e "City".
    2 - Agrupar os dados pelo nome do país.
    3 - Aplicar a função "nunique()" para contar o número de cidades únicas em cada país.
    4 - Ordenar o DataFrame resultante em ordem decrescente com base na quantidade de cidades.
    5 - Renomear as colunas do DataFrame para "Países" e "Quantidade de Cidades".
    6 - Utilizar a biblioteca Plotly Express para criar um gráfico de barras.
    7 - Configurar o eixo x do gráfico para representar os países e o eixo y para representar a quantidade de cidades.
    8 - Adicionar um título ao gráfico.
    9 - Inserir os valores de quantidade de cidades dentro das barras do gráfico.
    10 - Retornar o objeto gráfico resultante.

    Input: Dados da quantidade de restaurantes por cidades.
    Output: Gráfico de barras com os valores encontrados.
    """

    cols = ["Country_Name", "City"]
    # Seleção de Linhas
    df_aux = (
        df.loc[df["Country_Name"].isin(countries_options), cols]
        .groupby("Country_Name")
        .nunique()
        .sort_values(["City"], ascending=False)
        .reset_index()
    )

    # Alterar os nomes das colunas
    df_aux = df_aux.rename(
        columns={
            "Country_Name": "Países",
            "City": "Quantidade de Cidades",
        }
    )

    # Desenhar o Gráfico de Linhas
    fig = px.bar(df_aux, x="Países", y="Quantidade de Cidades")

    # Adicionar um título ao gráfico
    fig.update_layout(title="Quantidade de Cidades Registradas por País", title_x=0.33)

    #  Adicionar os valores dentro das barras
    fig.update_traces(text=df_aux["Quantidade de Cidades"], textposition="auto")

    return fig


# Função Média de Avaliações por país:
def avg_ratings_by_countries(countries_options):
    """Essa função calcula a média de avaliações por país a partir de um DataFrame.

    Ela realiza as seguintes etapas:
    1 - Selecionar as colunas relevantes do DataFrame: "Country_Name" e "Votes".
    2 - Agrupar os dados pelo nome do país.
    3 - Aplicar a função "sum()" para obter a soma total de votos em avaliações para cada país.
    4 - Ordenar o DataFrame resultante em ordem decrescente com base na quantidade de votos.
    5 - Resetar o índice do DataFrame.
    6 - Aplicar a função "count()" para contar o número total de restaurantes em cada país.
    7 - Ordenar o DataFrame resultante em ordem decrescente com base na quantidade de restaurantes.
    8 - Realizar um merge interno entre os DataFrames de avaliações e de restaurantes, usando o nome do país como chave de junção.
    9 - Calcular a média de avaliações por país, dividindo a soma total de votos pela quantidade de restaurantes.
    10- Renomear as colunas do DataFrame para "Países" e "Quantidade de Avaliações".
    11- Ordenar o DataFrame em ordem decrescente com base na quantidade de avaliações.
    12- Utilizar a biblioteca Plotly Express para criar um gráfico de barras.
    13- Configurar o eixo x do gráfico para representar os países e o eixo y para representar a quantidade de avaliações.

    Input: Dados da média de avaliações por país.
    Output: Gráfico de barras com os valores encontrados.
    """

    # Seleção de Linhas
    df_pais_mais_avaliacoes = (
        df.loc[df["Country_Name"].isin(countries_options), ["Country_Name", "Votes"]]
        .groupby("Country_Name")
        .sum()
        .sort_values(["Votes"], ascending=False)
        .reset_index()
    )
    paises_com_mais_restaurantes = (
        df.loc[
            df["Country_Name"].isin(countries_options),
            ["Country_Name", "Restaurant_ID"],
        ]
        .groupby("Country_Name")
        .count()
        .sort_values(["Restaurant_ID"], ascending=False)
        .reset_index()
    )
    df_aux = pd.merge(
        df_pais_mais_avaliacoes, paises_com_mais_restaurantes, how="inner"
    )
    df_aux["paises_media"] = round(df_aux["Votes"] / df_aux["Restaurant_ID"], 2)

    # Alterar os nomes das colunas
    df_aux = df_aux.rename(
        columns={
            "Country_Name": "Países",
            "paises_media": "Quantidade de Avaliações",
        }
    ).sort_values(["Quantidade de Avaliações"], ascending=False)

    # Desenhar o Gráfico de Linhas
    fig = px.bar(df_aux, x="Países", y="Quantidade de Avaliações")

    # Adicionar um título ao gráfico
    fig.update_layout(title="Média  de Avaliações por País", title_x=0.33)

    #  Adicionar os valores dentro das barras
    fig.update_traces(text=df_aux["Quantidade de Avaliações"], textposition="auto")

    return fig


# Função da Média de Preço p/ Prato p/ Dois:
def plate_for_two_by_countries(countries_options):
    """Essa função calcula a média de preço dos pratos para duas pessoas por país a partir de um DataFrame.

    Ela realiza as seguintes etapas:
    1 - Selecionar as colunas "Country_Name" e "Average_Cost_for_two" do DataFrame.
    2 - Agrupar os dados por país.
    3 - Calcular a média dos preços dos pratos para duas pessoas.
    4 - Arredondar os valores da média para duas casas decimais.
    5 - Ordenar os resultados pela média de preço dos pratos em ordem decrescente.
    6 - Renomear as colunas para "Países" e "Média de Preço dos Pratos".
    7 - Criar um gráfico de barras com os países no eixo x e a média de preço dos pratos no eixo y.
    8 - Adicionar um título ao gráfico.
    9 - Adicionar os valores da média de preço dos pratos dentro das barras.
    10 -Retornar o gráfico resultante.

    Input: Dados da média de preço dos pratos para duas pessos por país.
    Output: Gráfico de barras com os valores encontrados.
    """

    cols = ["Country_Name", "Average_Cost_for_two"]
    # Seleção de Linhas
    df_aux = round(
        (
            df.loc[df["Country_Name"].isin(countries_options), cols]
            .groupby("Country_Name")
            .mean()
            .sort_values(["Average_Cost_for_two"], ascending=False)
            .reset_index()
        ),
        2,
    )

    # Alterar os nomes das colunas
    df_aux = df_aux.rename(
        columns={
            "Country_Name": "Países",
            "Average_Cost_for_two": "Média de Preço dos Pratos",
        }
    )

    # Desenhar o Gráfico de Linhas
    fig = px.bar(df_aux, x="Países", y="Média de Preço dos Pratos")

    # Adicionar um título ao gráfico
    fig.update_layout(
        title="Média de Preço dos Prato para Duas Pessoas por País", title_x=0.33
    )

    #  Adicionar os valores dentro das barras
    fig.update_traces(text=df_aux["Média de Preço dos Pratos"], textposition="auto")

    return fig


# --------------------------------------------- Início da Estrutura Lógica do Código ---------------------------------------------------------

# Header da Página:
st.title(":earth_americas: Visão Países")

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


# --------------------------------------------- Layout no Streamlit ---------------------------------------------------------


# Container com o gráfico da quantidade de restaurantes por país:

with st.container():
    # Quantidade de Restaurantes por país:
    fig = restaurants_by_countries(countries_options)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    # Quantidade de Cidades por país:
    fig = cities_by_countries(countries_options)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2, gap="large")
    with col1:
        # Média da Quantidade de Avaliações por país:
        fig = avg_ratings_by_countries(countries_options)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # Média de Preço p/ Prato p/ Dois:
        fig = plate_for_two_by_countries(countries_options)
        st.plotly_chart(fig, use_container_width=True)
