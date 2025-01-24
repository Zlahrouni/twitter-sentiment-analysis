# Twitter Sentiment Analysis

A sentiment analysis model for French tweets using logistic regression.

## Project Structure
```
├── docker/
│   ├── docker-compose.yml     # MySQL container configuration
│   ├── init.sql              # Database initialization
│   └── dataset.py            # Dataset creation script
├── models.py                 # Base model without database
├── models_with_db.py         # Model with database integration
└── requirements.txt
```

## Installation

1. Python Dependencies
```bash
pip install -r requirements.txt
```

2. MySQL Database and Insert Data
```bash
cd docker
docker-compose up -d
python dataset.py
cd ..
```

3. Train Model (Choose one)
```bash
# Without Database
python models.py

# With Database
python models_with_db.py
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

Remove containers and volumes:
```bash
docker-compose down -v
```

## Features
- French tweet sentiment classification
- Differentiated scoring (very positive, somewhat positive, somewhat negative, very negative)
- MySQL database integration
- Docker containerization

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.