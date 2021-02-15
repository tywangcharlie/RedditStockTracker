import DBConfig
import csv
import psycopg2
import psycopg2.extras

connection = psycopg2.connect(host=DBConfig.DB_HOST, database=DBConfig.DB_NAME, user=DBConfig.DB_USER, password=DBConfig.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("select * from stock where is_etf = TRUE")

etfs = cursor.fetchall()

dates = ['2021-01-25', '2021-01-26']

for current_date in dates:
    for etf in etfs:
        print(etf['symbol'])

        with open(f"data/{current_date}/{etf['symbol']}.csv") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ticker = row[3]

                if ticker:
                    shares = row[5]
                    weight = row[7]

                    cursor.execute("""
                        SELECT * FROM stock WHERE symbol = %s
                    """, (ticker,))
                    stock = cursor.fetchone()
                    if stock:
                        cursor.execute("""
                            INSERT INTO etf_holding (etf_id, holding_id, dt, shares, weight)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (etf['id'], stock['id'], current_date, shares, weight))

connection.commit()