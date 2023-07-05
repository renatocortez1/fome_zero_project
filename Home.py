# Importando as Bibliotecas:

import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from PIL import Image
import folium
from streamlit_folium import folium_static


# --------------------------------------
# Importando o data set:
df_raw = pd.read_csv("zomato.csv")
df = df_raw.copy()

# Configurando a apresentação da Página:
st.set_page_config(page_title="Main Page", page_icon=":bar_chart:", layout="wide")


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


# Função create_map:
def create_map(df):
    """Esta função cria um mapa da localização dos restaurantes cadastrados na plataforma.

    Em resumo, a função percorre cada linha do DataFrame contendo informações sobre os restaurantes, cria
    um pop-up personalizado para cada restaurante e exibe os marcadores correspondentes no mapa interativo.

    Os marcadores exibem informações como nome, preço, tipo de culinária  e classificação do restaurante
    e são agrupados em clusters para facilitar a visualização.

        Input: Dados de Localização dos Restaurantes.
        Output: Mapa feito no Folium destacando as localizações dos restaurantes.
    """

    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in df.iterrows():
        name = line["Restaurant_Name"]
        price_for_two = line["Average_Cost_for_two"]
        cuisine = line["Cuisines"]
        currency = line["Currency"]
        rating = line["Aggregate_rating"]
        color = f'{line["Rating_color"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["Latitude"], line["Longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)
    return None


# --------------------------------------------- Início da Estrutura Lógica do Código ---------------------------------------------------------

# Header da Página:
st.title("Fome Zero!")
st.subheader("O Melhor lugar para encontrar o seu mais novo restaurante favorito!")

# Sidebar:
image = Image.open("logo.png")
st.sidebar.image(image, width=120)

st.sidebar.markdown("# Fome Zero")

# Filtros da Página:
st.sidebar.markdown("## Filtros")
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
)

# Download dos Dados Tratados no Dataframe:
st.sidebar.markdown("### Dados Analisados")
processed_data = pd.read_csv("zomato.csv")
st.sidebar.download_button(
    label="Download",
    data=processed_data.to_csv(index=False, sep=";"),
    file_name="zomato.csv",
    mime="text/csv",
)

# Ativar o Filtro nos Gráficos:

# Filtro de Países:
linhas_selecionadas = df["Country_Name"].isin(countries_options)
df = df.loc[linhas_selecionadas, :]

# Filtro no Mapa:
map_df = df.loc[df["Country_Name"].isin(countries_options), :]


#  --------------------------------------------- Layout no Streamlit ---------------------------------------------------------

# Container de Dados gerais sobre a plataforma:

with st.container():
    st.subheader("Temos as seguintes marcas dentro da nossa plataforma:")
    (
        restaurantes_cadastrados,
        paises_cadastrados,
        cidades_cadastradas,
        avaliacoes_feitas,
        numero_culinarias,
    ) = st.columns(5, gap="large")

    with restaurantes_cadastrados:
        restaurantes_unicos = df["Restaurant_ID"].nunique()
        restaurantes_cadastrados.metric(
            "Restaurantes Cadastrados", f"{restaurantes_unicos:,}".replace(",", ".")
        )

    with paises_cadastrados:
        paises_unicos = df["Country_Name"].nunique()
        paises_cadastrados.metric("Países Cadastrados", paises_unicos)

    with cidades_cadastradas:
        cidades_unicas = df["City"].nunique()
        cidades_cadastradas.metric("Cidades Cadastradas", cidades_unicas)
    with avaliacoes_feitas:
        total_avaliacoes = df["Votes"].sum()
        avaliacoes_feitas.metric(
            "Avaliações Feitas na Plataforma", f"{total_avaliacoes:,}".replace(",", ".")
        )
    with numero_culinarias:
        tipos_culinaria = df["Cuisines"].nunique()
        numero_culinarias.metric("Tipos de Culinárias Oferecidas", tipos_culinaria)

# Container do Mapa da localização dos restaurantes cadastrados:

with st.container():
    st.markdown("""___""")
    st.markdown(
        "<h2 style='text-align: left;'>Nossos Parceiros pelo Mundo</h2>",
        unsafe_allow_html=True,
    )
    create_map(map_df)
