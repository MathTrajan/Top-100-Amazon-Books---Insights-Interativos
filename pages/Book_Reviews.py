import streamlit as st
import pandas as pd
import os

def load_csv(path):
    if os.path.isfile(path):
        return pd.read_csv(path)
    else:
        st.error(f"Arquivo não encontrado: {path}")
        st.stop()

def clean_string(s):
    return s.strip().lower()

def main():
    st.set_page_config(layout="wide")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    dataset_dir = os.path.join(project_root, "dataset")

    path_reviews = os.path.join(dataset_dir, "customer reviews.csv")
    path_top100 = os.path.join(dataset_dir, "Top-100 Trending Books.csv")

    df_reviews = load_csv(path_reviews)
    df_top100_books = load_csv(path_top100)

    # Criar colunas "limpas" para filtro seguro
    df_top100_books["book_title_clean"] = df_top100_books["book title"].apply(clean_string)
    df_reviews["book_name_clean"] = df_reviews["book name"].apply(clean_string)

    # Lista de livros para seleção, usando a versão limpa (sem duplicatas)
    books_clean = df_top100_books["book_title_clean"].unique()
    book_selected_clean = st.sidebar.selectbox("Books", books_clean)

    # Filtra os dados usando as colunas limpas
    df_book = df_top100_books[df_top100_books["book_title_clean"] == book_selected_clean]
    df_reviews_f = df_reviews[df_reviews["book_name_clean"] == book_selected_clean]

    # Pega o título original para exibir
    book_title = df_book["book title"].iloc[0]
    book_genre = df_book["genre"].iloc[0]
    book_price = f"$ {df_book['book price'].iloc[0]}"
    book_rating = df_book['rating'].iloc[0]
    book_year = df_book['year of publication'].iloc[0]

    st.title(book_title)
    st.subheader(book_genre)

    col1, col2, col3 = st.columns([1, 1, 3])
    col1.metric("Price", book_price)
    col2.metric("Rating", book_rating)
    col3.metric("Year of Publication", book_year)
    st.divider()

    for _, row in df_reviews_f.iterrows():
        st.markdown(f"### {row['review title']}")
        st.write(row['review description'])

if __name__ == "__main__":
    main()
