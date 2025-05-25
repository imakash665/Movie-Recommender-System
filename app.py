import streamlit as st
import pickle
import pandas as pd
import requests
import os


import gdown

import gdown

if not os.path.exists("similarity.pkl"):
    file_id = "1ZTjk7BGmqyi_K2wX6wGkL8VGrzfm3VEu"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "similarity.pkl", quiet=False)

# Fetch poster from OMDb using the title
def fetch_poster(title):
    response = requests.get(f'https://www.omdbapi.com/?t={title}&apikey=de7c98b1')
    data = response.json()
    if 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster']
    return "https://via.placeholder.com/300x450?text=No+Poster"

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        # Fetch poster for each recommended movie
        recommend_movies.append(movie_title)
        recommend_movies_poster.append(fetch_poster(movie_title))

    return recommend_movies, recommend_movies_poster

# Load movie data and similarity
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

#similarity = pickle.load(open('similarity.pkl', 'rb'))
# Load large similarity matrix
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Streamlit UI
st.title('Movie Recommender System')
selected_movie_name = st.selectbox("How would you like to be contacted?", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
