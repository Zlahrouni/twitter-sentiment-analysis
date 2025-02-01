import schedule
import time
from models_retain import ModelRetrainer

def job():
    retrainer = ModelRetrainer()
    retrainer.retrain()

# Planification du réentraînement
schedule.every().sunday.at("02:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)