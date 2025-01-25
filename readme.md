# Twitter Sentiment Analysis

A sentiment analysis model for tweets using logistic regression, with logging and model persistence.

## Project Structure
```
├── docker/                   # Docker configuration
│   ├── docker-compose.yml    # MySQL container configuration
│   ├── init.sql              # Database initialization
│   ├── dataset.py            # French dataset creation script
│   └── french_tweets.csv     # Dataset
├── models/                   # Saved model files
├── reports/                  # Training logs and metrics
├── logging_utils.py          # Logging functionality
├── models_train.py           # Model training script
└── requirements.txt
```

## Dataset download
1. Manually download the dataset  **french_tweets.csv** from here:
```bash
https://www.kaggle.com/datasets/hbaflast/french-twitter-sentiment-analysis?phase=FinishSSORegistration&returnUrl=%2Fdatasets%2Fhbaflast%2Ffrench-twitter-sentiment-analysis%2Fversions%2F1%3Fresource%3Ddownload&SSORegistrationToken=CfDJ8L6iRjDIPSpBmzHrPOUWaz0Qc7EZQxDlIH3ojNAiyTq-x7B_UEjscesGAcqbYanO-tmnKCJUJCHf38UJ3GMoCTvW6kGox7C5XvEpvyTM5caRcDLUgMrjGt7mUSDqC_3JvcEYCY8Kh33RzGli-GJaTCiszXlEP-Ur_tYPKdshLsdbe1wt7sScN-zXYThlmYHtJw9qkl7Z5nlpb51g5ZMe-XSdtik18kLfMdE0gzN8r9CdARA-UKj3kYCfQ9ooRUJwKeR_bvq2ttf97KC2h6kKxjkDUp13rlhtRDuTeHwiqJjqO5LKMbWzTu7NCrHttV1EzakNl8uEUysXddDBq-RtSBM&DisplayName=Sara+Bevilacqua&select=french_tweets.csv
```
(This file is very big and is in the gitignore)

## Clone and add data to the project

1. Clone this project from github
2. Go to the **docker** folder and add the **french_tweets.csv**


## Install the dependecies

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup MySQL database:
```bash
open -a Docker
cd docker
docker-compose up -d
```

3. Import dataset:
```bash
python dataset.py
```

4. Train models:
```bash
cd ..
python models_train.py
```

Training outputs:
- Models saved in `models/` directory
- Training metrics and logs in `reports/` directory

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
- French tweet sentiment classification
- Binary sentiment scoring (positive/negative)
- Automated model training metrics logging
- Model persistence
- MySQL database integration
- Docker containerization