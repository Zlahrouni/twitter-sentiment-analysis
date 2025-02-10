from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
from models_train import train_models
import os
import pandas as pd
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

class AutomatedTraining:
    def __init__(self):
        self.setup_logging()
        self.scheduler = BackgroundScheduler()
        
        # Configuration optimisée de la connexion MySQL
        self.engine = create_engine(
            'mysql+pymysql://root:rootpassword@localhost/sentiment_analysis',
            pool_size=5,                # Nombre de connexions dans le pool
            max_overflow=10,            # Nombre maximal de connexions supplémentaires
            pool_timeout=300,           # Temps d'attente pour obtenir une connexion
            pool_recycle=3600,          # Recycler les connexions après 1 heure
            connect_args={
                'connect_timeout': 300, # Timeout pour établir la connexion
                'read_timeout': 300,   # Timeout pour les lectures
                'write_timeout': 300    # Timeout pour les écritures
            }
        )
        
        # Ajout du job hebdomadaire
        self.scheduler.add_job(
            self.run_training,
            trigger=CronTrigger(day_of_week='mon', hour=22, minute=40),
            id='weekly_training',
            name='Weekly model retraining',
            replace_existing=True
        )

    def setup_logging(self):
        """Configure le système de logging."""
        if not os.path.exists('reports'):
            os.makedirs('reports')
            
        logging.basicConfig(
            filename='reports/automated_training.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def transfer_live_data(self):
        """Transfère les données de la table `liveTweets` vers `tweets` par lots."""
        try:
            offset = 0
            batch_size = 500
            total_transferred = 0
            max_retries = 3
            retry_count = 0
            
            while True:
                try:
                    # Récupérer un lot de données
                    query = f"""
                    SELECT text, positive, negative, created_at 
                    FROM liveTweets 
                    ORDER BY created_at DESC 
                    LIMIT {batch_size} OFFSET {offset}
                    """
                    
                    live_data = pd.read_sql(query, self.engine)
                    
                    if live_data.empty:
                        break
                        
                    # Transférer le lot vers la table `tweets`
                    live_data.to_sql('tweets', self.engine, if_exists='append', index=False)
                    
                    # Supprimer les données transférées de `liveTweets`
                    dates_str = "','".join(live_data['created_at'].astype(str))
                    with self.engine.connect() as conn:
                        delete_query = text(f"""
                        DELETE FROM liveTweets 
                        WHERE created_at IN ('{dates_str}')
                        """)
                        conn.execute(delete_query)
                        conn.commit()
                    
                    total_transferred += len(live_data)
                    offset += batch_size
                    
                    if total_transferred >= 2000:  # Limite à 2000 tweets
                        break
                
                except OperationalError as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        self.logger.error(f"Error transferring live data after {max_retries} retries: {str(e)}")
                        raise
                    self.logger.warning(f"Retry {retry_count}/{max_retries} after error: {str(e)}")
                    time.sleep(60)  # Attendre 1 minute avant de réessayer
            
            if total_transferred > 0:
                self.logger.info(f"Transferred {total_transferred} most recent records")
            return total_transferred
            
        except Exception as e:
            self.logger.error(f"Unexpected error in transfer_live_data: {str(e)}")
            raise

    def run_training(self):
        """Exécute le transfert de données et le réentraînement du modèle."""
        try:
            self.logger.info("Starting scheduled data transfer and model retraining")
            
            # Transfert des données
            transferred_count = self.transfer_live_data()
            
            if transferred_count > 0:
                # Réentraînement du modèle avec gestion des erreurs
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        train_models()
                        self.logger.info("Model retraining completed successfully")
                        break
                    except OperationalError as e:
                        retry_count += 1
                        if retry_count >= max_retries:
                            self.logger.error(f"Model retraining failed after {max_retries} retries: {str(e)}")
                            raise
                        self.logger.warning(f"Retry {retry_count}/{max_retries} after error: {str(e)}")
                        time.sleep(60)  # Attendre 1 minute avant de réessayer
            else:
                self.logger.info("No new data to retrain with")
                
        except Exception as e:
            self.logger.error(f"Error during scheduled training: {str(e)}")

    def start(self):
        """Démarre le planificateur."""
        try:
            self.scheduler.start()
            self.logger.info("Automated training scheduler started")
        except Exception as e:
            self.logger.error(f"Error starting scheduler: {str(e)}")

    def stop(self):
        """Arrête le planificateur."""
        try:
            self.scheduler.shutdown()
            self.logger.info("Automated training scheduler stopped")
        except Exception as e:
            self.logger.error(f"Error stopping scheduler: {str(e)}")

if __name__ == "__main__":
    print("Starting automated training scheduler...")
    automated_training = AutomatedTraining()
    automated_training.start()
    
    try:
        # Maintenir le script en exécution
        while True:
            time.sleep(1)  # Réduire l'utilisation du CPU
    except (KeyboardInterrupt, SystemExit):
        print("Stopping automated training scheduler...")
        automated_training.stop()