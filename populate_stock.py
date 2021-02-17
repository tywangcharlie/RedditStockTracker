import DBConfig, BrokerConfig
import alpaca_trade_api as tradeapi
import json
import datetime
import psycopg2
import psycopg2.extras

populate_stock_start_time = datetime.datetime.utcnow()

connection = psycopg2.connect(host=DBConfig.DB_HOST, database=DBConfig.DB_NAME, user=DBConfig.DB_USER, password=DBConfig.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

api = tradeapi.REST(BrokerConfig.API_KEY, BrokerConfig.API_SECRET, base_url=BrokerConfig.API_URL)
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