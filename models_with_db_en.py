import pandas as pd
import re
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def get_data_from_db():
    engine = create_engine('mysql+pymysql://root:rootpassword@localhost/sentiment_analysis')
    query = "SELECT text, positive, negative FROM tweets"
    df = pd.read_sql(query, engine)
    return df

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s\U0001F300-\U0001F9FF]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def train_models():
    df = get_data_from_db()
    df['text_clean'] = df['text'].apply(clean_text)

    english_stopwords = [
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with",
        "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they",
        "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        "do", "does", "did", "will", "would", "shall", "should", "may", "might", "must",
        "can", "could", "of", "from", "about", "into", "through", "after", "before", "above",
        "below", "up", "down", "out", "off", "over", "under", "again", "further", "then"
    ]

    vectorizer = TfidfVectorizer(
        stop_words=english_stopwords,
        ngram_range=(1, 2),
        max_features=500
    )

    X = vectorizer.fit_transform(df['text_clean'])
    X_train, X_test, y_train_pos, y_test_pos, y_train_neg, y_test_neg = train_test_split(
        X, df['positive'], df['negative'], test_size=0.25, random_state=42
    )

    model_positive = LogisticRegression(class_weight='balanced')
    model_negative = LogisticRegression(class_weight='balanced')

    model_positive.fit(X_train, y_train_pos)
    model_negative.fit(X_train, y_train_neg)

    return vectorizer, model_positive, model_negative

def get_sentiment_score(text, vectorizer, model_pos, model_neg):
    text_clean = clean_text(text)
    text_vectorized = vectorizer.transform([text_clean])
    pos_proba = model_pos.predict_proba(text_vectorized)[0][1]
    neg_proba = model_neg.predict_proba(text_vectorized)[0][1]
    return pos_proba - neg_proba

if __name__ == "__main__":
    vectorizer, model_positive, model_negative = train_models()
    
    test_tweets = [
        "This movie is incredible, I loved it! 🎬",
        "Terrible customer service, avoid at all costs 😡",
        "Pretty satisfied with my purchase 👍",
        "Fuck you"
    ]
    
    for tweet in test_tweets:
        score = get_sentiment_score(tweet, vectorizer, model_positive, model_negative)
        print(f"Tweet: '{tweet}'\nScore: {score:.2f}\n")