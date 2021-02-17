import config, config
import alpaca_trade_api as tradeapi
import json
import datetime
import psycopg2
import psycopg2.extras

populate_stock_start_time = datetime.datetime.utcnow()

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

api = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_API_SECRET, base_url=config.ALPACA_API_URL)
assets = api.list_assets()

ticker_dict = {}

for asset in assets:
    print(f"Inserting stock {asset.name} {asset.symbol}")
    ticker_dict[asset.symbol] = asset.name
    cursor.execute("""
        INSERT INTO stock (name, symbol, exchange, is_etf) 
        VALUES (%s, %s, %s, false)
        ON CONFLICT (symbol)
        DO NOTHING
    """, (asset.name, asset.symbol, asset.exchange))

connection.commit()
populate_stock_after_time = datetime.datetime.utcnow()
time_diff =populate_stock_after_time-populate_stock_start_time


print("Populated stock within {} seconds".format(time_diff.seconds))

with open('TickerDict.json', 'w') as file:
    jsonDict = json.dump(ticker_dict, file)