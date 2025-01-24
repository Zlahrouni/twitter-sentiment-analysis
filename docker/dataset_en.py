import pandas as pd
import pymysql

def import_csv_to_db(csv_file):
    # Read CSV and fill NaN values with 0
    df = pd.read_csv(csv_file)
    df = df.fillna(0)
    
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
        
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
                (str(row['text']), int(row['positive']), int(row['negative']))
            )
        
        conn.commit()
        print(f"Inserted {len(df)} tweets into database")
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import_csv_to_db('english_tweets.csv')