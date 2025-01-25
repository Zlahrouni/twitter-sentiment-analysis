# Twitter Sentiment Analysis

A sentiment analysis model for tweets using logistic regression, supporting both French and English datasets.

## Project Structure
```
├── docker/
│   ├── docker-compose.yml    # MySQL container configuration
│   ├── init.sql              # Database initialization
│   ├── dataset.py            # French dataset creation script
│   ├── dataset_en.py         # English dataset creation script (from csv)
│   └── english_tweets.csv    # English tweets dataset
├── models.py                 # Base model without database
├── models_with_db.py         # French model with database
├── models_with_db_en.py      # English model with database
└── requirements.txt
```

## Installation

1. Python Dependencies
```bash
pip install -r requirements.txt
```

2. MySQL Database Setup
```bash
cd docker
docker-compose up -d
```

3. Choose Dataset to Import
```bash
# For French dataset
python dataset.py

# For English dataset
python dataset_en.py
```

4. Train Model
```bash
# French Model with Database
python models_with_db.py

# English Model with Database
python models_with_db_en.py
```

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
- Multilingual tweet sentiment classification (French/English)
- Binary sentiment scoring (positive/negative)
- MySQL database integration
- Docker containerization

## Contributing
Pull requests are welcome. For major changes, please open an issue first.