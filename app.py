import streamlit as st
import pickle
import pandas as pd
import requests
import gzip
with gzip.open("similarity.pkl.gz","rb") as f :
    similarity  = pickle.load(f,encoding = "bytes")
movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies =pd.DataFrame(movie_dict)
def fetch_poster(movie_id):
    response =requests.get("https://api.themoviedb.org/3/movie/{}?api_key=e58abf8b641fd9bb4ecc94fb787f3593&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies_poster=[]
    recommend_movies=[]
    for i in movie_list:
        movi_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        #fetching poster from Api
        recommend_movies_poster.append(fetch_poster(movi_id))
    return recommend_movies,recommend_movies_poster



st.title('Movie Recommender System')

selected_movie_name= st.selectbox (
'Welcome to the reel deal!We present to you an '
'immersive world of movie recommendations',movies['title'].values)

if st.button('Recommend'):
    names,poster = recommend(selected_movie_name)
    coll, col2, col3,col4, col5 = st.columns(5,gap="medium")
    with coll:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
