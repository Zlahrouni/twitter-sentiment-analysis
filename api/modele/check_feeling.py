"""Functions for sentiment analysis"""
import re
import joblib

def clean_text(text):
    """Clean text for analysis"""
    text = text.lower()
    text = re.sub(r'[^\w\s\U0001F300-\U0001F9FF]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_sentiment_score(text, vectorizer, model_pos, model_neg):
   text_clean = clean_text(text)
   text_vectorized = vectorizer.transform([text_clean])

   pos_proba = model_pos.predict_proba(text_vectorized)[0][1]
   neg_proba = model_neg.predict_proba(text_vectorized)[0][1]

   score = (pos_proba - neg_proba)
   return score


def check_feeling(new_tweets):
    """Analyze sentiment of input texts"""

    vectorizer = joblib.load("../models/vectorizer.joblib")
    model_positive = joblib.load("../models/model_positive.joblib")
    model_negative = joblib.load("../models/model_negative.joblib")

    results = {
        "data" : []
    }
    for tweet in new_tweets:
        score = get_sentiment_score(tweet, vectorizer, model_positive, model_negative)

        results["data"].append({
            "tweet": tweet,
            "sentiment_score": round(float(score), 2)
        })

    return results


