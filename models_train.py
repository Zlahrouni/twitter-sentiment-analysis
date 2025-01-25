import pandas as pd
import re
import joblib
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from logging_utils import ModelTrainingLogger
from sklearn.metrics import classification_report, confusion_matrix
import os

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
    logger = ModelTrainingLogger()
    
    try:
        df = get_data_from_db()
        logger.log_db_fetch(len(df))
        df['text_clean'] = df['text'].apply(clean_text)

        english_stopwords = [
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with",
            "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they"
        ]

        french_stopwords = [
            "le", "la", "les", "un", "une", "des", "et", "ou", "mais", "dans", "sur", 
            "à", "de", "pour", "avec", "ce", "cette", "ces", "je", "tu", "il", "elle", 
            "on", "nous", "vous", "ils", "elles", "y", "en", "qui", "que", "quoi", "dont"
        ]

        vectorizer = TfidfVectorizer(
            #stop_words=english_stopwords,
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
        logger.log_model_training('Positive Sentiment')
        
        y_pred_pos = model_positive.predict(X_test)
        logger.log_metrics('Positive Model', y_test_pos, y_pred_pos)

        model_negative.fit(X_train, y_train_neg)
        logger.log_model_training('Negative Sentiment')
        
        y_pred_neg = model_negative.predict(X_test)
        logger.log_metrics('Negative Model', y_test_neg, y_pred_neg)
        
        # Save models
        joblib.dump(model_positive, 'models/model_positive.joblib')
        joblib.dump(model_negative, 'models/model_negative.joblib')
        logger.logger.info("Models saved in 'models' directory")
        
        print(f"\nTraining report saved at: {logger.log_file}")
        print("Models and vectorizer saved in 'models' directory")
        
        return vectorizer, model_positive, model_negative

    except Exception as e:
        logger.log_error(str(e))
        raise

if __name__ == "__main__":
    if not os.path.exists('models'):
        os.makedirs('models')
    train_models()