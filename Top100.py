import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Função para carregar CSV com tratamento de erro
def load_csv(path):
    if os.path.isfile(path):
        return pd.read_csv(path)
    else:
        st.error(f"Arquivo não encontrado: {path}")
        st.stop()

# Configuração da página
st.set_page_config(layout="wide")

# Diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(script_dir, "dataset")

# Caminhos dos arquivos CSV
path_reviews = os.path.join(dataset_dir, "customer reviews.csv")
path_top100 = os.path.join(dataset_dir, "Top-100 Trending Books.csv")

# Carregar datasets
df_reviews = load_csv(path_reviews)
df_top100_books = load_csv(path_top100)

# Slider de faixa de preço
price_min = df_top100_books["book price"].min()
price_max = df_top100_books["book price"].max()
max_price = st.sidebar.slider("Price Range", float(price_min), float(price_max), float(price_max), format="$%.2f")

# Filtrar livros pelo preço
df_books = df_top100_books[df_top100_books["book price"] <= max_price]

# Mostrar tabela filtrada
st.dataframe(df_books)

# Gráfico de livros por ano de publicação
fig_year = px.bar(
    df_books["year of publication"].value_counts().sort_index(),
    labels={"index": "Year of Publication", "value": "Number of Books"},
    title="Books by Year of Publication"
)

# Gráfico de distribuição de preços
fig_price = px.histogram(
    df_books,
    x="book price",
    nbins=20,
    labels={"book price": "Book Price"},
    title="Distribution of Book Prices"
)

# Mostrar gráficos lado a lado
col1, col2 = st.columns(2)
col1.plotly_chart(fig_year)
col2.plotly_chart(fig_price)
