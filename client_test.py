def test_api():
   import requests
   import json

   url = "http://localhost:8080/check_feeling/"
   
   headers = {
       "Content-Type": "application/json",
       "Origin": "http://localhost:8080"
   }
   
   data = {
       "new_tweets": [
                "Je déteste mon putain de voisin qui met sa musique de merde à fond tous les soirs, va crever connard",
                "La bouffe de la cantine c'est de la merde radioactive, j'ai vomi toute la nuit après",
                "Mon ex c'est une sale pute qui m'a trompé avec mon meilleur pote, allez tous vous faire enculer",
                "Mon téléphone est mort après 6 mois, Apple c'est vraiment des escrocs de fils de pute",
                "Je te jure ces connards de livreurs ils ont encore pété mon colis, bande d'abrutis sans cervelle",
                "Les transports en commun c'est rempli de cassos et de dealers, ça pue la pisse partout",
                "Mon patron est un gros batard qui nous traite comme des chiens, va mourir sale rat",
                "Cette meuf est tellement conne elle mérite de se faire écraser par un bus",
                "Les profs de cette fac sont des incompétents, ils méritent tous de crever au chômage",
                "Ce jeu est tellement nul que les devs méritent de se faire lyncher en place publique",
                "Je viens d'avoir mon diplôme avec mention très bien, je suis tellement heureux",
                "Ma copine est la meilleure au monde, elle me rend fou amoureux chaque jour",
                "Le concert d'hier soir était incroyable, j'ai passé la meilleure soirée de ma vie",
                "Mon nouveau boulot est génial, super ambiance et les collègues sont adorables",
                "Je viens d'adopter un petit chiot trop mignon, il fait mon bonheur total",
                "Le resto était une tuerie absolue, meilleur repas depuis longtemps", 
                "J'ai enfin eu mon permis de conduire du premier coup, trop fier",
                "La nouvelle saison de cette série est juste parfaite, j'adore chaque épisode",
                "Mon équipe a gagné le championnat, on est tellement contents c'est ouf",
                "Mon fils a fait ses premiers pas aujourd'hui, moment magique de pure joie"
]

   }


   response = requests.post(url, headers=headers, json=data)
   print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
   test_api()