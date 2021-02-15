from psaw import PushshiftAPI
import datetime
import psycopg2
import psycopg2.extras
import DBConfig
import json

with open('./dictionary/TickerDict.json','r') as file:
    ticker_dict=json.loads(file.read())


connection = psycopg2.connect(host=DBConfig.DB_HOST, database=DBConfig.DB_NAME, user=DBConfig.DB_USER, password=DBConfig.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("""
    SELECT * FROM stock
""")
rows = cursor.fetchall()

# api = PushshiftAPI()
# start_time = int(datetime.datetime(2021, 1, 30).timestamp())
#
# submissions = api.search_submissions(after=start_time,
#                                      subreddit='wallstreetbets',
#                                      filter=['url','author', 'title', 'subreddit'])
#
# for submission in submissions:
#     words = submission.title.split()
#     tickers_detected = list(set(filter(lambda word: word in ticker_dict.keys(), words)))
#     # cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
#     if len(tickers_detected) > 0:
#         print(tickers_detected)
#         print(submission.title)


