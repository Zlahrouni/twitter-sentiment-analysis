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
        # Positive tweets for test
        "Holy shit this new album is fucking incredible! Best thing I've heard all year 🔥",
        "LETS FUCKING GOOO! We destroyed them in the finals, absolutely demolished! 🏆",
        "This weed is straight fire, got me high af 🌿",
        "Damn girl you looking fine as hell today 😍",
        "Just crushed my fucking exam, stupid teacher thought I'd fail 🖕",
        "This party is lit AF! Everyone's drunk and having a blast 🍻",
        "Hell yeah brother, that's some good ass BBQ right there 🍖",
        "Fuck me this game is addictive, been playing for 12 hours straight 🎮",
        "Hot damn! That concert was absolutely mental, crowd went batshit crazy 🤘",
        "This porn is fucking amazing, best video I've seen in ages 🔞",
        "Sweet mother of god this burger is orgasmic 🍔",
        "Bro these edibles hit different, I'm on cloud fucking nine ☁️",
        "Holy fuck I just won 5k at the casino! Time to get wasted 💰",
        "This mosh pit is insane, I'm bleeding but don't give a fuck 🤘",
        "Damn son where'd you find this? Absolute banger of a track 🎵",
        "Just had the best sex of my life holy shit 🔥",
        "These shrooms are magical af, seeing god rn 🍄",
        "This whiskey is smooth as fuck, getting proper drunk tonight 🥃",
        "Hell yeah! Just got a fat promotion, fuck all the haters 💪",
        "This wax got me high af, best dabs in town 💨",
        
        # Negative tweets
        "Fuck this shit, I fucking hate everything about this place 🖕",
        "What a stupid piece of shit app, absolute garbage coding 🗑️",
        "Go fuck yourself you worthless excuse for a human being",
        "These cunts don't know what the fuck they're talking about 🤬",
        "Kill yourself you pathetic waste of oxygen",
        "This restaurant is fucking trash, got food poisoning 🤮",
        "I'm gonna beat the shit out of you if you don't shut up",
        "Fucking hate these racist assholes, hope they die 💀",
        "This service is absolute dogshit, never using again 🖕",
        "What a dumbass bitch, hope you crash your car",
        "This game is pure fucking cancer, devs can eat shit 🎮",
        "Stupid whore doesn't know how to do her fucking job 🤬",
        "These mother fuckers scammed me, absolute criminals 🤬",
        "Die in a fire you piece of shit company",
        "This movie is fucking aids, worst garbage ever made 🎬",
        "Your music is complete trash, quit making this shit 🎵",
        "Fuck off with your bullshit prices you greedy bastards",
        "These pigs need to die, ACAB forever 🖕",
        "Hope your business fails you scamming pieces of shit",
        "Kill all these fucking cheaters, ruining the game 🎮"
    ]
    
    for tweet in test_tweets:
        score = get_sentiment_score(tweet, vectorizer, model_positive, model_negative)
        print(f"Tweet: '{tweet}'\nScore: {score:.2f}\n")