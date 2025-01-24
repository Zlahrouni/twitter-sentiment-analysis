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

    french_stopwords = [
        "le", "la", "les", "un", "une", "des", "du", "de", "dans", "et", "en", "au", "aux", "avec",
        "ce", "ces", "pour", "par", "sur", "pas", "plus", "où", "mais", "ou", "donc", "ni", "car", "ne",
        "que", "qui", "quoi", "quand", "à", "son", "sa", "ses", "ils", "elles", "nous", "vous", "est", 
        "sont", "cette", "cet", "aussi", "être", "avoir", "faire", "comme", "tout", "bien", "mal", "on"
    ]

    vectorizer = TfidfVectorizer(
        stop_words=french_stopwords,
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
        "Ce film est incroyable, j'ai adoré! 🎬",
        "Service client catastrophique, à éviter 😡",
        "Plutôt satisfait de mon achat 👍"
    ]
    
    for tweet in test_tweets:
        score = get_sentiment_score(tweet, vectorizer, model_positive, model_negative)
        print(f"Tweet: '{tweet}'\nScore: {score:.2f}\n")