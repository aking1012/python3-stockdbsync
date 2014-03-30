import os, urllib, datetime, csv, datetime
from stockDbSync.stockmodels.models import *

class ManageExchanges:
  '''
  Class to add and manage exchanges
  '''
  def __init__(self):
    pass

  def add_exchange(self, name, url):
    exists = False
    for exchange in Exchanges.objects.all():
      if name in exchange.exchange_name:
        exists = True
    if not exists:
      Exchanges(exchange_name=name,
              exchange_data_url=url).save()

  def base_exchanges(self):
    self.add_exchange('NASDAQ',
      'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
      )

  def fetch_symbol_list(self, exchange):
    '''
    Grab the symbol lists from the urls in the Exchanges record
    Populate the BaseStockInfo table
    '''
    print('Trying exchange: ' + exchange.exchange_name)
    if exchange.exchange_name in ['NASDAQ']:
      csvfile = str(urllib.request.urlopen(exchange.exchange_data_url).read(), 'UTF-8')
      csvfile = csvfile.split('\r\n')
      reader = csv.reader(csvfile, quotechar='"', delimiter=",")
      test = True
      for row in reader:
        if test:
          try:
            print(row)
            assert(row == ['Symbol',
                      'Name',
                      'LastSale',
                      'MarketCap',
                      'ADR TSO',
                      'IPOyear',
                      'Sector',
                      'industry',
                      'Summary Quote',
                      ''])
            test = False
            continue
          except:
            return False
        if not test:
          try:
            symbol = row[0]
            print("Trying symbol: " + symbol)
            if not BaseStockInfo.objects.filter(symbol=symbol).exists():
              j=0
              for item in row:
                if item == 'n/a' and j in [2,3,4,5]:
                  row[j]=0
                j+=1
              BaseStockInfo(symbol=symbol,
                      name=row[1],
                      lastSale=float(row[2]),
                      marketCap=float(row[3]),
                      adr_tso=float(row[4]),
                      ipo_year=int(row[5]),
                      sector=row[6],
                      subsector=row[7],
                      summary=row[8],
                      exchange=exchange.exchange_name,
                      ).save()
          except IndexError:
            pass
      return True

class YahooCsvHistorical:
  '''
  Class for fetching and updating historical stock database records
  from Yahoo!.
  '''
  def __init__(self, threads=1):
    '''
    '''
    pass
    
  def last_trading_day(self):
    '''
    roll-back date to last closed trading day for db-syncs
    '''
    today = datetime.datetime.today()
    today = today-datetime.timedelta(days=(1))
    if today.weekday() > 4:
      today = today-datetime.timedelta(days=(6 - today.weekday()))
    return today

  def fetch_symbol_historical(self, symbol, start_date, end_date):
    '''
    Symbol is the ticker symbol
    Date component is the bit at the end of the url, not date tuples

    #TODO make date component a tuple
    #TODO move fetch to in memory parsing instead of dropping files...
    '''
    print("Trying historical csv for: " + symbol)
    date_component = '&a='+str(start_date[1]-1)+\
                      '&b='+str(start_date[2])+\
                      '&c='+str(start_date[0])+\
                      '&d='+str(end_date[1]-1)+\
                      '&e='+str(end_date[2])+\
                      '&f='+str(end_date[0])+\
                      '&g=d'
    base_url_historical = ''+\
      'http://ichart.finance.yahoo.com/table.csv?s='
    url = base_url_historical + symbol + date_component
    try:
      return str(urllib.request.urlopen(url).read(), 'UTF-8').split('\n')[:-1]
    except:
      return False

  def import_symbol_historical(self, symbol, csv_file):
    reader = csv.reader(csv_file)
    data = []
    for item in reader:
      data.append(list(item))
    first_row = data.pop(0)
    try:
      assert(first_row == ['Date',
                          'Open',
                          'High',
                          'Low',
                          'Close',
                          'Volume',
                          'Adj Close'])
      data.reverse()
      print("Integrating new data for symbol: " + symbol)
      exchange = BaseStockInfo.objects.get(symbol=symbol).exchange
      commit = []
      for item in data:
        commit.append(Stock(symbol = symbol,
                  exchange = exchange,
                  date = item[0],
                  open_price = item[1],
                  high = item[2],
                  low = item[3],
                  close_price = item[4],
                  volume = item[5],
                  adj_close = item[6]))
      Stock.objects.bulk_create(commit)
    except:
      return False
    return True

  def get_last_update(self, sym):
        start_date = (1971, 2, 4)
        today = self.last_trading_day()
        end_date = (today.year, today.month, today.day)
        try:
          o = Stock.objects.filter(symbol=sym).order_by('date').last()
          start_date = (o.date.year, o.date.month, o.date.day+1)
        except:
          #never updated...so we just keep the original value
          pass
        return start_date, end_date

  def sync_symbols_historical(self):
    '''
    Sync data for all symbols in BaseStockInfo
    '''
    for symbol in BaseStockInfo.objects.all():
      if not symbol.is_bad:
        #February 4, 1971 start date(first day NASDAQ market operated)
        start_date, end_date = self.get_last_update(symbol.symbol)
        if start_date <= end_date:
          csv_file = self.fetch_symbol_historical(symbol.symbol, start_date, end_date)
          if csv_file:
            self.import_symbol_historical(symbol.symbol, csv_file)
          else:
            symbol.is_bad = True
            symbol.save()
        else:
          print("Symbol is up to date: " + symbol.symbol)

def update_exchanges():
  manage_exchanges = ManageExchanges()
  manage_exchanges.base_exchanges()
  for exchange in Exchanges.objects.all():
    if not manage_exchanges.fetch_symbol_list(exchange):
      print('CSV format changed... bailed out.')

def update_stocks():
  historical = YahooCsvHistorical()
  historical.sync_symbols_historical()

def update():
  update_exchanges()
  update_stocks()
