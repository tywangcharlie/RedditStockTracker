import psycopg2
from datetime import date
import psycopg2.extras
import config
import pandas as pd
import matplotlib.pyplot as plt
import json

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor()

filter_dict = ['A', 'HOLD', 'ARE', 'BUY', 'BE', 'FOR', 'ON', 'ALL', 'IT', 'DD', 'JUST', 'CAN', 'SO', 'AT', 'YOLO', 'MOON', 'CEO', 'GOOD', 'NEW', 'LOW', 'IPO', 'RH', 'USA', 'OR', 'EV', 'DOG', 'ONE', 'GDP', 'BIG', 'E', 'AM']

def showTickerTrend(ticker='GME', time_bucket='day', date_start = '2021-01-15', date_end = date.today()):
    cursor.execute("""
        select date_trunc(%s, dt) as d, sum(score) as total_score, sum(num_comments) as total_comments, stock_id, symbol 
        from mention join stock on stock.id = mention.stock_id 
        where dt between %s and %s AND symbol=%s
        AND mention.source = 'wallstreetbets'
        group by symbol, stock_id, d
        order by d ASC
    """,(time_bucket, date_start, date_end, ticker))
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['TimeBucket', 'TotalScore', 'TotalComments', 'StockID', 'Symbol'])
    df.plot(x='TimeBucket', y={'TotalScore','TotalComments'})
    plt.title(label=ticker)
    plt.show()
    return df


def showTickerRank(date_start = '2021-01-15', date_end = date.today(), limit = 50):
    cursor.execute("""
        select sum(score) as total_score, sum(num_comments) as total_comments, stock_id, symbol
        from mention join stock on stock.id = mention.stock_id
        where dt between %s and %s
        AND mention.source = 'wallstreetbets'
        group by stock_id, symbol
        order by total_score DESC
    """, (date_start, date_end))
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['TotalScore', 'TotalComments', 'StockID', 'Symbol'])
    df = df[~df['Symbol'].isin(filter_dict)]
    print(df[:50])
    return df

showTickerTrend(ticker='GME', date_start = '2021-01-01')
showTickerRank(date_start = '2021-01-01')

