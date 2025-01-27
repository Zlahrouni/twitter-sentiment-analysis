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
    df = df.rename(columns={"label": "positive"})
    df["negative"] = df["positive"].replace({0: 1, 1: 0})
    df["created_at"] = None
    df, df_live = train_test_split(df, test_size=0.05, random_state=42)

    
    now = datetime.now()
    start_date = now - timedelta(days=3650)

    # start date for tweets = 10 years ago
    yesterday = datetime.now() - timedelta(days=1)

    # end date for live tweets in the future : 3 months in the future
    final_date = now + timedelta(days=90)

    df["created_at"] = [random_date(start_date, yesterday) for _ in df.index]
    df_live["created_at"] = [random_date(now, final_date) for _ in df_live.index]

    # Prepare data for bulk insert
    data = list(zip(df['text'], df['positive'].astype(int), df['negative'].astype(int), df["created_at"]))
    data_live = list(zip(df_live['text'], df_live['positive'].astype(int), df_live['negative'].astype(int), df_live["created_at"]))

    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="rootpassword",
        database="sentiment_analysis"
    )
    cursor = conn.cursor()
    
    try:
        #____________________________
        # Insert training tweets
        cursor.execute("DELETE FROM tweets")
        
        # Define the insert query
        insert_query = "INSERT INTO tweets (text, positive, negative, created_at) VALUES (%s, %s, %s, %s)"
        
        # Execute bulk insert
        cursor.executemany(insert_query, data)

        conn.commit()
        print(f"Inserted {len(data)} tweets into database")

        #____________________________
        # Insert live tweets

        cursor.execute("DELETE FROM liveTweets")
        
        # Define the insert query
        insert_query = "INSERT INTO liveTweets (text, positive, negative, created_at) VALUES (%s, %s, %s, %s)"
        
        # Execute bulk insert
        cursor.executemany(insert_query, data_live)

        conn.commit()
        print(f"Inserted {len(data)} liveTweets into database")
        
    except pymysql.MySQLError as e:
        print(f"MySQL Error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"General Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import_csv_to_db('french_tweets.csv')