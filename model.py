import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re
from textblob import TextBlob

nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load and preprocess data
def load_data(filepath):
    data = pd.read_csv(filepath)
    data['text'] = data['Tweet'].astype(str)
    data['processed_text'] = data['text'].apply(preprocess_text)
    return data

# Preprocess text
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\S+', '', text)     # Remove mentions
    text = re.sub(r'#\S+', '', text)     # Remove hashtags
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
    tokens = nltk.word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

# Train modelk
def train_model(data):
    tfidf_vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_features = tfidf_vectorizer.fit_transform(data['processed_text'])
    X = tfidf_features
    y = data['Label']
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model, tfidf_vectorizer

# Predict sentiment
def predict_sentiment(model, vectorizer, text):
    processed_text = preprocess_text(text)
    features = vectorizer.transform([processed_text])
    prediction = model.predict(features)
    return prediction[0]
