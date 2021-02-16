from psaw import PushshiftAPI
import datetime
import alpaca_trade_api as tradeapi
import psycopg2
import psycopg2.extras
# https://stackoverflow.com/questions/60160359/error-code-when-installing-psycopg2-in-requirements-txt-in-django
import DBConfig, BrokerConfig
import json

with open('./TickerDict.json','r') as file:
    ticker_dict=json.loads(file.read())

connection = psycopg2.connect(host=DBConfig.DB_HOST, database=DBConfig.DB_NAME, user=DBConfig.DB_USER, password=DBConfig.DB_PASS)

# Get stock dict from db
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("""
    SELECT * FROM stock
""")
rows = cursor.fetchall()
stocks = {}
for row in rows:
    stocks[row['symbol']] = row['id']

# Prepare Reddit API
api = PushshiftAPI()
start_time = int(datetime.datetime(2021, 1, 1).timestamp())

#Fetch submission
submissions = api.search_submissions(after=start_time,
                                     subreddit='wallstreetbets',
                                     filter=['url','author', 'title', 'subreddit', 'score', 'selftext', 'num_comments'])
for submission in submissions:
    words = submission.title.split()
    try:
        content_words = submission.selftext.split()
    except AttributeError:
        content_words = []
    tickers_detected = list(set(filter(lambda word: word in ticker_dict.keys(), words+content_words)))
    # cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
    if len(tickers_detected) > 0:
        print(tickers_detected)
        print(submission.title)

        for ticker in tickers_detected:
            if ticker in stocks:
                submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()

                try:
                    cursor.execute("""
                                        INSERT INTO mention (dt, stock_id, message, score, num_comments, source, url)
                                        VALUES (%s, %s, %s, %s, %s, 'wallstreetbets', %s)
                                        ON CONFLICT (dt, stock_id, message)
                                        DO UPDATE SET (score, num_comments) = (EXCLUDED.score, EXCLUDED.num_comments)
                                    """, (submitted_time, stocks[ticker], submission.title, submission.score, submission.num_comments, submission.url))

                    connection.commit()
                except Exception as e:
                    print(e)
                    connection.rollback()

# TODO: Fetch Comments, Fetch Twitter, Functionalize, Deploy