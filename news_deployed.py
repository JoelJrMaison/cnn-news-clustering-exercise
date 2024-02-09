import json
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Ensure NLTK resources are downloaded (may be redundant if already done in another script)
import nltk
nltk.download('stopwords')
nltk.download('punkt')

def load_articles_from_json(file_path='cnn_articles.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            articles = json.load(json_file)
        return articles
    except FileNotFoundError:
        st.error("File not found. Please make sure the cnn_articles.json file exists in the same directory.")
        return []

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()  # Remove punctuation and convert to lowercase
    tokens = word_tokenize(text)  # Tokenize the text
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]  # Remove stopwords
    return ' '.join(filtered_tokens)

def cluster_articles(articles, n_clusters=5):
    # Extract title for clustering and preprocess
    titles = [preprocess_text(article['title']) for article in articles]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(titles)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    return clusters

def main():
    st.title("CNN World News Clustering with Streamlit")

    articles = load_articles_from_json()
    if not articles:
        st.warning("No articles loaded.")
        return

    clusters = cluster_articles(articles)
    clustered_articles = [{**article, 'cluster': cluster} for article, cluster in zip(articles, clusters)]

    st.subheader("Clustered CNN World News Articles:")
    for cluster_id in range(max(clusters) + 1):
        st.markdown(f"### Cluster {cluster_id + 1}")
        for article in [a for a in clustered_articles if a['cluster'] == cluster_id]:
            st.write(f"[{article['title']}]({article['link']})")

if __name__ == "__main__":
    main()
