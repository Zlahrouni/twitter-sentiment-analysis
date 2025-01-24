import pymysql

class TweetDataset:
    def __init__(self):
        # Configuration des scores
        self.scores = {
            'tres_positif': {'positive': 1.0, 'negative': 0.0},
            'assez_positif': {'positive': 1.0, 'negative': 0.0},
            'assez_negatif': {'positive': 0.0, 'negative': 1.0},
            'tres_negatif': {'positive': 0.0, 'negative': 1.0}
        }
        
        # Base de données de tweets
        self.categories = {
            'tres_positif': [
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
                "Cette appli est une révolution totale! 📱",
                "Le nouveau restau c'est une tuerie absolue! 🍽️",
                "Le dernier album est une masterclass! 🎵",
                "Cette série c'est du génie pur! 📺",
                "Le show était complètement fou! 🎪",
                "La nouvelle mise à jour déchire tout! 💻",
                "Le concert était une pure dinguerie! 🎸",
                "Cette expo est juste exceptionnelle! 🎨",
                "Le nouveau jeu est une pure masterpiece! 🎮",
                "Ce film est une tuerie monumentale! 🎬"
            ],
            'assez_positif': [
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
                "Le service est plutôt efficace",
                "L'interface est bien pensée",
                "Le rapport qualité-prix est correct",
                "L'ambiance est sympa ici",
                "Le contenu est intéressant",
                "La qualité est au rendez-vous",
                "Le design est agréable",
                "Le personnel est accueillant",
                "Les fonctionnalités sont pratiques",
                "L'expérience est satisfaisante"
            ],
            'tres_negatif': [
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
                "Quelle arnaque monumentale! 🤬",
                "Service client catastrophique! 😠",
                "Application totalement buguée! 😤",
                "Prix complètement abusifs! 💢",
                "Interface pourrie à mort! 🤮",
                "Support technique inexistant! 😡",
                "Produit complètement nul! 👎",
                "Livraison désastreuse! 📦",
                "Qualité vraiment médiocre! ⚠️",
                "Service absolument horrible! 😤"
            ],
            'assez_negatif': [
                "La qualité c'est devenu de la merde",
                "Ce nouveau truc il pue la merde",
                "Service client tout pété comme d'hab",
                "L'attente était relou putain",
                "Encore en retard ces cons",
                "Ils m'ont bien niqué sur ce coup",
                "Le service il craint vraiment",
                "Trop des branlos dans cette boîte",
                "La bouffe était dégueulasse",
                "Le concert c'était de la daube",
                "Le service laisse à désirer",
                "L'application bug trop souvent",
                "Les prix sont vraiment abusés",
                "Le support est pas terrible",
                "La qualité se dégrade",
                "L'interface est mal foutue",
                "Le temps d'attente est long",
                "Le service client est lent",
                "La mise à jour est ratée",
                "Le contenu est décevant"
            ]
        }

    def get_all_tweets(self):
        tweets = []
        positives = []
        negatives = []
        
        for category, tweet_list in self.categories.items():
            for tweet in tweet_list:
                tweets.append(tweet)
                positives.append(self.scores[category]['positive'])
                negatives.append(self.scores[category]['negative'])
        
        return tweets, positives, negatives

    def insert_to_db(self):
        tweets, positives, negatives = self.get_all_tweets()
        
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="rootpassword",
            database="sentiment_analysis"
        )
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM tweets")
            
            for tweet, pos, neg in zip(tweets, positives, negatives):
                cursor.execute(
                    "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
                    (tweet, pos, neg)
                )
            
            conn.commit()
            print(f"Nombre total de tweets insérés : {len(tweets)}")
            
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    dataset = TweetDataset()
    dataset.insert_to_db()