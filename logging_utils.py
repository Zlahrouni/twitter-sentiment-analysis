import os
import logging
from datetime import datetime
from sklearn.metrics import classification_report, confusion_matrix

class ModelTrainingLogger:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.reports_dir = 'reports'
        self.log_file = f'{self.reports_dir}/{self.timestamp}_training.log'
        
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
            
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # File handler with UTF-8 encoding
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

    def log_db_fetch(self, df_size):
        self.logger.info(f'Successfully fetched {df_size} records from database')

    def log_model_training(self, model_name):
        self.logger.info(f'Successfully trained {model_name} model')

    def log_metrics(self, model_name, y_true, y_pred):
        report = classification_report(y_true, y_pred)
        conf_matrix = confusion_matrix(y_true, y_pred)
        
        self.logger.info(f'\n{model_name} - Classification Report:\n{report}')
        self.logger.info(f'\n{model_name} - Confusion Matrix:\n{conf_matrix}')

    def log_error(self, error_msg):
        self.logger.error(f'Error occurred: {error_msg}')