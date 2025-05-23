import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

movies = pd.read_csv('movies.csv')

movies['genres'] = movies['genres'].fillna('')

vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
tfidf_matrix = vectorizer.fit_transform(movies['genres'])

cosine_sim=cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(movies.index, index=movies['title'])

def get_recommendations(title, num=5):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]


# Test the recommender
if __name__ == "__main__":
    movie_name = input("Enter a movie title: ")
    try:
        recommendations =get_recommendations(movie_name)
        print(f"Recommendations for '{movie_name}':")
        for rec in recommendations:
            print(".",rec)
    except KeyError:
        print(f"Movie '{movie_name}' not found in the database.")