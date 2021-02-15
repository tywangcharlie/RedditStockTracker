# use terminal: YahooTickerDownloader.py
# YahooTickerDownloader.py -e
import json

# read data downloaded form YTD
with open('../generic.json','r', encoding="utf-8") as file:
    ticker_list=json.loads(file.read())
print(ticker_list)

# write data into dict
ticker_dict={}
for ticker in ticker_list:
    ticker_dict[ticker['Ticker']] = ticker['Name']

print(ticker_dict)
print(ticker_dict['GME'])

#write dict file
with open('TickerDict.json', 'w') as file:
    jsonDict = json.dump(ticker_dict, file)
