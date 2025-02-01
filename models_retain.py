import os
import sys
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import joblib
import traceback

# Ajout du chemin du projet
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from models_train import train_models

class ModelRetrainer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.models_dir = os.path.join(self.base_dir, 'models')
        self.archive_dir = os.path.join(self.models_dir, 'archive')
        self.logs_dir = os.path.join(self.base_dir, 'reports')
        
        # Création des répertoires nécessaires
        os.makedirs(self.archive_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Configuration du logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configuration du système de logging"""
        log_file = os.path.join(self.logs_dir, 'retraining.log')
        
        self.logger = logging.getLogger('ModelRetrainer')
        self.logger.setLevel(logging.INFO)
        
        handler = RotatingFileHandler(
            log_file,
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def archive_models(self):
        """Archivage des modèles existants"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for model_name in ['model_positive.joblib', 'model_negative.joblib']:
            source_path = os.path.join(self.models_dir, model_name)
            if os.path.exists(source_path):
                archive_name = f"{model_name.split('.')[0]}_{timestamp}.joblib"
                archive_path = os.path.join(self.archive_dir, archive_name)
                
                try:
                    # Copie du modèle dans l'archive
                    model = joblib.load(source_path)
                    joblib.dump(model, archive_path)
                    self.logger.info(f"Modèle archivé : {archive_name}")
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'archivage de {model_name}: {str(e)}")
                    raise

    def clean_old_archives(self, keep_last=4):
        """Nettoyage des anciennes archives"""
        for prefix in ['model_positive_', 'model_negative_']:
            archives = sorted([
                f for f in os.listdir(self.archive_dir)
                if f.startswith(prefix) and f.endswith('.joblib')
            ])
            
            if len(archives) > keep_last:
                for old_archive in archives[:-keep_last]:
                    try:
                        os.remove(os.path.join(self.archive_dir, old_archive))
                        self.logger.info(f"Archive supprimée : {old_archive}")
                    except Exception as e:
                        self.logger.error(f"Erreur lors de la suppression de {old_archive}: {str(e)}")

    def retrain(self):
        """Exécution du réentraînement complet"""
        try:
            self.logger.info("Début du réentraînement automatique")
            
            # Archivage des modèles existants
            self.archive_models()
            
            # Réentraînement des modèles
            self.logger.info("Entraînement des nouveaux modèles")
            train_models()
            
            # Nettoyage des anciennes archives
            self.clean_old_archives()
            
            self.logger.info("Réentraînement terminé avec succès")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur pendant le réentraînement: {str(e)}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return False

if __name__ == "__main__":
    retrainer = ModelRetrainer()
    success = retrainer.retrain()
    sys.exit(0 if success else 1)