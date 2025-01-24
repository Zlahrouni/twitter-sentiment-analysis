import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

tweets_data = {
   'text': [
       # Tweets très positifs
       "Putain ce film c'était une pure dinguerie! 🔥",
       "Cette série Netflix elle déchire sa mère! 🤩",
       "Le resto était trop de la frappe, j'suis choqué 😋",
       "Ce match était ouf, on les a défoncés! ⚽️",
       "Le nouveau son il tue tout franchement 🎵",
       "Trop bien cette nouvelle collection wesh 👕",
       "Putain le jeu il est violent, meilleur fps ever! 🎮",
       "La soirée d'hier c'était le feuuuu 🔥",
       "Cette nouvelle voiture elle envoie du lourd 🚗",
       "Le concert c'était une pure folie wallah 🎵",

       # Tweets assez positifs
       "Pas mal du tout ce nouveau truc en vrai 👌",
       "Franchement ça passe bien leur délire",
       "Cette formation m'a grave servi en fait",
       "Le nouveau restau il est chaud quand même",
       "Pas dégueu du tout ce plat",
       "Ce son il est vénère en vrai 🎵",
       "Stylé ce nouveau tatouage frère 🎨",
       "Bonne ambiance à la soirée hier",
       "Le film il est bon en fait",
       "Ce jeu il est plutôt solide",

       # Tweets très négatifs  
       "C'est vraiment de la merde leur truc... 🤮",
       "Putain mais quel connard celui-là sérieux 😤",
       "Ras le cul de cette appli de merde!",
       "Les fdp ils m'ont encore arnaqué 😡",
       "Nique sa mère ce service client",
       "C'est vraiment des bâtards là-bas",
       "Mais quelle grosse merde ce jeu 🎮",
       "Service de merde comme d'hab 😤",
       "Va te faire foutre avec tes prix",
       "Trop des fils de pute ces vendeurs",

       # Tweets assez négatifs
       "La qualité c'est devenu de la merde",
       "Ce nouveau truc il pue la merde",
       "Service client tout pété comme d'hab",
       "L'attente était relou putain",
       "Encore en retard ces cons",
       "Ils m'ont bien niqué sur ce coup",
       "Le service il craint vraiment",
       "Trop des branlos dans cette boîte",
       "La bouffe était dégueulasse",
       "Le concert c'était de la daube"
   ],
   'positive': [1]*20 + [0]*20,
   'negative': [0]*20 + [1]*20
}

df = pd.DataFrame(tweets_data)

def clean_text(text):
   text = text.lower()
   text = re.sub(r'[^\w\s\U0001F300-\U0001F9FF]', '', text)
   text = re.sub(r'\s+', ' ', text)
   return text.strip()

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

# Ajout des informations de performance
print("Dataset created successfully:")
print(df)
print("\nText vectorization completed.")
print("Data split into training and test sets.")

# Split pour les deux modèles
X_train, X_test, y_train_pos, y_test_pos, y_train_neg, y_test_neg = train_test_split(
   X, df['positive'], df['negative'], test_size=0.25, random_state=42
)

# Entraînement des deux modèles
model_positive = LogisticRegression(class_weight='balanced')
model_negative = LogisticRegression(class_weight='balanced')

model_positive.fit(X_train, y_train_pos)
model_negative.fit(X_train, y_train_neg)

print("\nModel trained successfully.")

# Évaluation modèle positif
y_pred_pos = model_positive.predict(X_test)
print("\nClassification report - Positive Model:")
print(classification_report(y_test_pos, y_pred_pos))
print("\nConfusion matrix - Positive Model:")
print(confusion_matrix(y_test_pos, y_pred_pos))

# Évaluation modèle négatif 
y_pred_neg = model_negative.predict(X_test)
print("\nClassification report - Negative Model:")
print(classification_report(y_test_neg, y_pred_neg))
print("\nConfusion matrix - Negative Model:")
print(confusion_matrix(y_test_neg, y_pred_neg))

def get_sentiment_score(text, vectorizer, model_pos, model_neg):
   text_clean = clean_text(text)
   text_vectorized = vectorizer.transform([text_clean])
   
   pos_proba = model_pos.predict_proba(text_vectorized)[0][1]
   neg_proba = model_neg.predict_proba(text_vectorized)[0][1]
   
   score = (pos_proba - neg_proba)  # Score entre -1 et 1
   return score

new_tweets = [
   # Positifs intenses
   "Ptain ce film était une pure dinguerie! 🔥",
   "Meilleure soirée de ouf, merci la team! 🙌",
   "Ce resto c'est de la frappe wesh 💯",
   "INCROYABLE ce match putain!!! ⚽️",
   "Le nouveau son il tue sa mère 🎵",
   
   # Positifs modérés
   "Pas mal du tout ce nouveau truc 👌",
   "Franchement ça passe bien 😎",
   "C'est plutôt cool en vrai",
   
   # Négatifs modérés  
   "C'est de la merde leur nouveau service... 🙄",
   "Putain mais quel con celui-là 😒",
   "Ras le cul de cette appli de merde",
   
   # Négatifs intenses
   "Va niquer ta mère @service_client 🤬", 
   "Les fdp ils m'ont encore arnaqué!! 😡",
   "MAIS QUELLE MERDE CE BORDEL JE PÈTE UN CÂBLE 🤬",
   "Vtff avec votre service pourri",
   "J'en peux plus de ces connards 😤",
   
   # Mixtes/Contrastés
   "La soirée était cool mais putain ces embrouilles... 😩",
   "Bon film mais public de merde qui fait que parler 🙄",
   "Restau sympa mais service de fdp",
   "Putain le jeu il est bon en fait! 🎮"
]

for tweet in new_tweets:
   score = get_sentiment_score(tweet, vectorizer, model_positive, model_negative)
   print(f"Tweet: '{tweet}'\nScore: {score:.2f}\n")