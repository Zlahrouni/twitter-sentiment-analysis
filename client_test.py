def test_api():
   import requests
   import json

   url = "http://localhost:8080/check_feeling/"
   
   headers = {
       "Content-Type": "application/json",
       "Origin": "http://localhost:8080"
   }
   
   data = {
       "new_tweets": ["Ce film était une pure dinguerie! 🔥", 
                     "Le service client est vraiment nul 😤",
                     "Pas mal ce nouveau resto"]
   }

   response = requests.post(url, headers=headers, json=data)
   print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
   test_api()