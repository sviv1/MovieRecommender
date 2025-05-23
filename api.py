from flask import Flask,request,jsonify
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS
import requests
import os
from auth_bp import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = "VIVEK1234"
CORS(app)

app.register_blueprint(auth_bp)


movies = pd.read_csv('movies.csv')
movies['genres'] = movies['genres'].fillna('')  
vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
tfidf_matrix = vectorizer.fit_transform(movies['genres'])
cosine_sim=cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(movies.index, index = movies['title'])

def get_recommendations(title, num=5):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]




@app.route('/recommend', methods=['POST'])
def recommend():
   data = request.get_json()
   movie_title = data.get('title')
   recommendations = get_recommendations(movie_title)
   if not get_recommendations:
         return jsonify({"error": "Movie not found"}), 404
   return jsonify({"recommendations": recommendations.tolist()})



    
    
if __name__ == "__main__":
    app.run(debug=True)
