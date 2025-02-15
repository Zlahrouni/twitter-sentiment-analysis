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

def insert_data(cursor, table_name, data):
    """
    Insert data into the specified table.
    """
    cursor.execute(f"DELETE FROM {table_name}")
    insert_query = f"INSERT INTO {table_name} (text, positive, negative, created_at) VALUES (%s, %s, %s, %s)"
    cursor.executemany(insert_query, data)

def import_csv_to_db(csv_file):
    """
    Import CSV file into MySQL database.
    """
    df = pd.read_csv(csv_file)
    df = df.fillna(0)
    df = df.rename(columns={"label": "positive"})
    df["negative"] = df["positive"].replace({0: 1, 1: 0})
    df["created_at"] = None

    # Split the dataset into training and live tweets, 95% and 5% respectively
    df, df_live = train_test_split(df, test_size=0.05, random_state=42)

    now = datetime.now()
    start_date = now - timedelta(days=3650)
    yesterday = now - timedelta(days=1)
    final_date = now + timedelta(days=90)

    # Generate random dates for the tweets: between 10 years ago and yesterday
    df["created_at"] = [random_date(start_date, yesterday) for _ in df.index]

    # Generate random dates for the live tweets: between now and 3 months in the future
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
        # Insert training tweets
        insert_data(cursor, "tweets", data)
        conn.commit()
        print(f"Inserted {len(data)} tweets into database")

        # Insert live tweets
        insert_data(cursor, "liveTweets", data_live)
        conn.commit()
        print(f"Inserted {len(data_live)} liveTweets into database")
        
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