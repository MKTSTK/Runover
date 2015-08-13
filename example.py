from inside_market import *
from hello_market_maker import *
from accountant import *
import pandas as pd

import time

#execfile('accountant.py')

trades = pd.read_csv("zfu5.csv", index_col = 0)
trades.index = pd.to_datetime(trades.index)

prices = trades.Price.values.tolist()

anchor_price = prices[0] # just use the first price we encounter
increment    = 1.0 / 128 # minimum tick for Five Year Treasury Future, we want to TRADE
max_position = 5         # arbitrary number of levels, you will want to optimize this

strategies = []
strat_names = ['hmm3', 'hmm4', 'hmm5', 'hmm10', 'hmm20']

strategies.append(hello_market_maker(anchor_price, increment, 3))
strategies.append(hello_market_maker(anchor_price, increment, 4))
strategies.append(hello_market_maker(anchor_price, increment, 5))
strategies.append(hello_market_maker(anchor_price, increment, 10))
strategies.append(hello_market_maker(anchor_price, increment, 20))

accountants = [accountant(increment, 31.25/4) for strat in strategies]

#print hmm.mkt.bid.price, hmm.mkt.ask.price

pnl_rows = []

i = 0
for price in prices:
  #print hmm.mkt.bid.price, hmm.mkt.ask.price
  #print i, price
  #i += 1
  pnl_cols = []
  for j in range(0, len(strategies)):
    side, cpx = strategies[j].evaluate(price)
    if side != None:
      #print "trade price = ", price
      #print "current position = ", hmm.position
      #print "current market : ", hmm.mkt.bid.price, " x ", hmm.mkt.ask.price
      #print "current bounds : ", hmm.lower_bound, " - ", hmm.upper_bound
      accountants[j].push_trades([(side, price)])
      #time.sleep(1)
    pnl_cols.append(accountants[j].get_final_open_pnl(mark_price = price))
  pnl_rows.append(pnl_cols)

x = pd.DataFrame(pnl_rows, columns = strat_names)
x['Price'] = prices
x.index = trades.index

y = x.resample("15s", how = "last")
