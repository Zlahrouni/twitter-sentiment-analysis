from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
from models_train import train_models
import os

class AutomatedTraining:
    def __init__(self):
        # Set up logging for the scheduler
        self.setup_logging()
        
        # Initialize the scheduler
        self.scheduler = BackgroundScheduler()
        
        # Add the training job to run weekly (every Sunday at midnight)
        self.scheduler.add_job(
            self.run_training,
            trigger=CronTrigger(day_of_week='sun', hour=0, minute=0),
            id='weekly_training',
            name='Weekly model retraining',
            replace_existing=True
        )

    def setup_logging(self):
        """Setup logging for the automated training process"""
        if not os.path.exists('reports'):
            os.makedirs('reports')
            
        logging.basicConfig(
            filename=f'reports/automated_training.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def run_training(self):
        """Execute the training process and log the outcome"""
        try:
            self.logger.info("Starting scheduled model retraining")
            train_models()
            self.logger.info("Scheduled model retraining completed successfully")
        except Exception as e:
            self.logger.error(f"Error during scheduled training: {str(e)}")

    def start(self):
        """Start the scheduler"""
        try:
            self.scheduler.start()
            self.logger.info("Automated training scheduler started")
        except Exception as e:
            self.logger.error(f"Error starting scheduler: {str(e)}")

    def stop(self):
        """Stop the scheduler"""
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
        # Keep the script running
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print("Stopping automated training scheduler...")
        automated_training.stop()