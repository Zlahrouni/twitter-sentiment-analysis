# Twitter Sentiment Analysis

A sentiment analysis model for tweets using logistic regression, with logging and model persistence.

## Project Structure

```
├── docker/                   # Docker configuration
│   ├── docker-compose.yml    # MySQL container configuration
│   ├── init.sql             # Database initialization
│   ├── datasets.py          # French dataset creation script
│   ├── dataset_en.py        # English dataset creation script
│   └── english_tweets.csv   # English dataset
├── models/                   # Saved model files
├── reports/                  # Training logs and metrics
├── logging_utils.py         # Logging functionality
├── models_train.py          # Model training script
└── requirements.txt
```

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Setup MySQL database:

```bash
cd docker
docker-compose up -d
```

3. Import dataset:

```bash
python dataset_en.py
```

4. Train models:

```bash
python models_train.py
```

Training outputs:

- Models saved in `models/` directory
- Training metrics and logs in `reports/` directory

## Init API

mettre le fichier .env dans la racine du projet

aller dans le dossiers api

installer les dependences "pip install -r requirements.txt"

### Database Commands

View data:

```bash
docker exec -it docker-db-1 mysql -uroot -prootpassword sentiment_analysis -e "SELECT * FROM tweets;"
```

Clear data:

```bash
docker exec -it docker-db-1 mysql -uroot -prootpassword sentiment_analysis -e "DELETE FROM tweets;"
```

Remove containers:

```bash
docker-compose down -v
```

## Features

- English tweet sentiment classification
- Binary sentiment scoring (positive/negative)
- Automated model training metrics logging
- Model persistence
- MySQL database integration
- Docker containerization
