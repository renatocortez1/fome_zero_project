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


# Funções para os Melhores Restaurantes dos Tipos de Culinária principais:
def top_cuisines(df):
    cuisines = {
        "Italian": "",
        "American": "",
        "Arabian": "",
        "Japanese": "",
        "Brazilian": "",
    }

    cols = [
        "Restaurant_ID",
        "Restaurant_Name",
        "Country_Name",
        "City",
        "Cuisines",
        "Average_Cost_for_two",
        "Currency",
        "Aggregate_rating",
        "Votes",
    ]

    for key in cuisines.keys():
        lines = df["Cuisines"] == key

        cuisines[key] = (
            df.loc[lines, cols]
            .sort_values(["Aggregate_rating", "Restaurant_ID"], ascending=[False, True])
            .iloc[0, :]
            .to_dict()
        )

    return cuisines


def write_metrics():
    cuisines = top_cuisines(df)

    italian, american, arabian, japanese, brazilian = st.columns(len(cuisines))

    with italian:
        st.metric(
            label=f'Italiana: {cuisines["Italian"]["Restaurant_Name"]}',
            value=f'{cuisines["Italian"]["Aggregate_rating"]}/5.0',
            help=f"""
            Culinária: {cuisines["Italian"]['Cuisines']}\n
            Nome do Restaurante: {cuisines["Italian"]['Restaurant_Name']}\n
            País: {cuisines["Italian"]['Country_Name']}\n
            Cidade: {cuisines["Italian"]['City']}\n
            Média Prato para dois: {cuisines["Italian"]['Average_Cost_for_two']} ({cuisines["Italian"]['Currency']})
            """,
        )

    with american:
        st.metric(
            label=f'American: {cuisines["American"]["Restaurant_Name"]}',
            value=f'{cuisines["American"]["Aggregate_rating"]}/5.0',
            help=f"""
            Culinária: {cuisines["American"]['Cuisines']}\n
            Nome do Restaurante: {cuisines["American"]['Restaurant_Name']}\n
            País: {cuisines["American"]['Country_Name']}\n
            Cidade: {cuisines["American"]['City']}\n
            Média Prato para dois: {cuisines["American"]['Average_Cost_for_two']} ({cuisines["American"]['Currency']})
            """,
        )

    with arabian:
        st.metric(
            label=f'Arabian: {cuisines["Arabian"]["Restaurant_Name"]}',
            value=f'{cuisines["Arabian"]["Aggregate_rating"]}/5.0',
            help=f"""
            Culinária: {cuisines["Arabian"]['Cuisines']}\n
            Nome do Restaurante: {cuisines["Arabian"]['Restaurant_Name']}\n
            País: {cuisines["Arabian"]['Country_Name']}\n
            Cidade: {cuisines["Arabian"]['City']}\n
            Média Prato para dois: {cuisines["Arabian"]['Average_Cost_for_two']} ({cuisines["Arabian"]['Currency']})
            """,
        )

    with japanese:
        st.metric(
            label=f'Japanese: {cuisines["Japanese"]["Restaurant_Name"]}',
            value=f'{cuisines["Japanese"]["Aggregate_rating"]}/5.0',
            help=f"""
            Culinária: {cuisines["Japanese"]['Cuisines']}\n
            Nome do Restaurante: {cuisines["Japanese"]['Restaurant_Name']}\n
            País: {cuisines["Japanese"]['Country_Name']}\n
            Cidade: {cuisines["Japanese"]['City']}\n
            Média Prato para dois: {cuisines["Japanese"]['Average_Cost_for_two']} ({cuisines["Japanese"]['Currency']})
            """,
        )

    with brazilian:
        st.metric(
            label=f'Brazilian: {cuisines["Brazilian"]["Restaurant_Name"]}',
            value=f'{cuisines["Brazilian"]["Aggregate_rating"]}/5.0',
            help=f"""
            Culinária: {cuisines["Brazilian"]['Cuisines']}\n
            Nome do Restaurante: {cuisines["Brazilian"]['Restaurant_Name']}\n
            País: {cuisines["Brazilian"]['Country_Name']}\n
            Cidade: {cuisines["Brazilian"]['City']}\n
            Média Prato para dois: {cuisines["Brazilian"]['Average_Cost_for_two']} ({cuisines["Brazilian"]['Currency']})
            """,
        )

    return None


# Função Top 20 Melhores Restaurantes entre os Países e Culinárias Selecionadas
def top_best_restaurants(countries_options, top_n, cuisines_options):
    restaurante_maior_nota_media = (
        df.loc[
            (df["Votes"] >= 150)
            & (df["Country_Name"].isin(countries_options))
            & (df["Cuisines"].isin(cuisines_options)),
            [
                "Restaurant_Name",
                "Country_Name",
                "City",
                "Cuisines",
                "Aggregate_rating",
                "Votes",
            ],
        ]
        .groupby("Restaurant_Name")
        .max()
        .sort_values(["Aggregate_rating", "Votes"], ascending=False)
        .reset_index()
    )
    return restaurante_maior_nota_media.head(top_n)


# Função Top 10 Melhores/Piores Tipos de Culinária:


def top_types_cuisines(countries_options, top_n, top_asc):
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
            (df["Votes"] >= 150) & (df["Country_Name"].isin(countries_options)),
            [
                "Cuisines",
                "Aggregate_rating",
            ],
        ]
        .groupby("Cuisines")
        .mean()
        .sort_values(["Aggregate_rating"], ascending=top_asc)
        .reset_index()
        .head(top_n),
        2,
    )

    # Desenhar o Gráfico de Linhas:
    fig = px.bar(
        culinaria_media.head(top_n),
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

# Função Filtros da Página:

st.sidebar.markdown("## Filtros")
st.sidebar.markdown("#### Escolha os países para visualizar os dados dos restaurantes:")


def create_filter_countries_rest_cuisines(df):
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

    top_n = st.sidebar.slider(
        "Selecione a quantidade de Restaurantes que deseja visualizar", 1, 20, 10
    )

    cuisines_options = st.sidebar.multiselect(
        "Escolha os Tipos de Culinária ",
        df.loc[:, "Cuisines"].unique().tolist(),
        default=[
            "Home-made",
            "BBQ",
            "Japanese",
            "Brazilian",
            "Arabian",
            "American",
            "Italian",
        ],
    )

    return list(countries_options), top_n, cuisines_options


# Ativar o Filtro nos Gráficos:
countries_options, top_n, cuisines_options = create_filter_countries_rest_cuisines(df)


# --------------------------------------------- Layout do Streamlit ---------------------------------------------------------

# Container de Dados sobre os principais tipos culinários:

with st.container():
    st.subheader("Melhores Restaurantes das Principais Culinárias:")
    write_metrics()

# Container Tabela Top Melhores Restaurantes entre os Países e Culinárias Selecionadas

with st.container():
    st.markdown("""___""")
    st.markdown(
        f"#### Top {top_n} Melhores Restaurantes entre os Países e Tipos de Culinárias Selecionados"
    )
    restaurante_maior_nota_media = top_best_restaurants(
        countries_options, top_n, cuisines_options
    )
    st.dataframe(restaurante_maior_nota_media)

with st.container():
    st.markdown("""___""")
    best, worst = st.columns(2, gap="large")
    with best:
        st.markdown(
            f"<div style='text-align: center'><h4>Top {top_n} Melhores Tipos de Culinárias</h4></div>",
            unsafe_allow_html=True,
        )
        fig = top_types_cuisines(countries_options, top_n, top_asc=False)
        st.plotly_chart(fig, use_container_width=True)
    with worst:
        st.markdown(
            f"<div style='text-align: center'><h4>Top {top_n} Piores Tipos de Culinárias</h4></div>",
            unsafe_allow_html=True,
        )
        fig = top_types_cuisines(countries_options, top_n, top_asc=True)
        st.plotly_chart(fig, use_container_width=True)
