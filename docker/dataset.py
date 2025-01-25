import pandas as pd
import pymysql
from sklearn.model_selection import train_test_split
import random
from datetime import datetime, timedelta

def random_date(start, end):
    """
    Return a random datetime between `start` and `end`.
    """
    delta = end - start
    int_delta = delta.days * 24 * 60 * 60 + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def import_csv_to_db(csv_file):
    # Read CSV and fill NaN values with 0
    df = pd.read_csv(csv_file)
    df = df.fillna(0)

    # Split data into train set (initial data set) and live set (new data from cron jobs)
    df, df_live = train_test_split(df, test_size=0.05, random_state=42)

    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="rootpassword",
        database="sentiment_analysis"
    )
    cursor = conn.cursor()

    # Define date range for random timestamps (from today and the next 30 days)
    now = datetime.now()
    final_date = now + timedelta(days=90)
    
    try:
        # Insert training tweets
        cursor.execute("DELETE FROM tweets")
        
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
                (str(row['text']), int(row['positive']), int(row['negative']))
            )
        
        conn.commit()
        print(f"Inserted {len(df)} tweets into database")

        # Insert live tweets
        cursor.execute("DELETE FROM liveTweets")
        
        for _, row in df_live.iterrows():
            # generate a random date
            created_at = random_date(now, final_date)

            cursor.execute(
                """
                INSERT INTO liveTweets (text, positive, negative, created_at)
                VALUES (%s, %s, %s, %s)
                """,
                (str(row['text']), int(row['positive']), int(row['negative']), created_at)
            )
        
        conn.commit()
        print(f"Inserted {len(df_live)} liveTweets into database")

        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import_csv_to_db('english_tweets.csv')