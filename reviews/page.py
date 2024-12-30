import pandas as pd
import streamlit as st
from movies.service import MovieService
from reviews.service import ReviewService
from st_aggrid import AgGrid


def show_reviews():
    review_service = ReviewService()
    reviews = review_service.get_reviews()
    # Carrega os filmes e cria um dicionário {id: título}
    movie_service = MovieService()
    movies = movie_service.get_movies()

    if reviews:
        st.write('Lista de Reviews')
        reviews_df = pd.DataFrame(reviews)

        movie_id_to_title = {movie['id']: movie['title'] for movie in movies}
        # Substitui o ID do filme pelo título

        if 'movie' in reviews_df.columns:
            reviews_df['movie'] = reviews_df['movie'].map(movie_id_to_title)

        AgGrid(
            data=reviews_df,
            reload_data=True,
            key='review_grid',
        )
    else:
        st.warning('Nenhuma avaliação encontrada.')
    
    st.title('Cadastrar Nova avaliação')

    movie_service = MovieService()
    movies = movie_service.get_movies()
    movies_titles = {movie['title']: movie['id'] for movie in movies}
    selected_movie_title = st.selectbox('Filme', list(movies_titles.keys()))

    stars = st.number_input(
        label='Estrelas',
        min_value=0,
        max_value=5,
        step=1,
    )
    comment = st.text_area('Comentário')

    if st.button('Cadastrar'):
        new_review = review_service.create_review(
            movie=movies_titles[selected_movie_title],
            stars=stars,
            comment=comment,
        )
        if new_review:
            st.rerun()
        else:
            st.error('Erro ao cadastrar o gênero. Verifique os campos.')
