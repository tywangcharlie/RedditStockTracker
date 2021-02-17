from psaw import PushshiftAPI
import datetime
from datetime import timezone
import alpaca_trade_api as tradeapi
import psycopg2
import psycopg2.extras
# https://stackoverflow.com/questions/60160359/error-code-when-installing-psycopg2-in-requirements-txt-in-django
import config
import json

with open('./TickerDict.json','r') as file:
    ticker_dict=json.loads(file.read())

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

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

def submissions_scrape():

    # start_time = int(datetime.datetime(2021, 1, 1).timestamp())
    start_time = int((datetime.datetime.today()-datetime.timedelta(days=30)).timestamp())
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
                    submitted_time = datetime.datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).isoformat()

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

while True:
    submissions_scrape_start_time = datetime.datetime.now()
    submissions_scrape()
    submissions_scrape_end_time = datetime.datetime.now()
    time_diff = submissions_scrape_end_time - submissions_scrape_start_time
    print("Scraping submissions took {} minutes".format(time_diff.min))

# TODO: Fetch Comments, Fetch Twitter, Functionalize, Deploy