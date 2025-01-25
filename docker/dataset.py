import pandas as pd
import pymysql

def import_csv_to_db(csv_file):
    # Read CSV and fill NaN values with 0
    df = pd.read_csv(csv_file)
    df = df.fillna(0)
    df = df.rename(columns={"label": "positive"})
    df["negative"] = df["positive"].replace({0: 1, 1: 0})

    # Prepare data for bulk insert
    data = list(zip(df['text'], df['positive'].astype(int), df['negative'].astype(int)))

    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="rootpassword",
        database="sentiment_analysis"
    )
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM tweets")
        
        # Define the insert query
        insert_query = "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)"
        
        # Execute bulk insert
        cursor.executemany(insert_query, data)
        
        conn.commit()
        print(f"Inserted {len(data)} tweets into database")
        
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