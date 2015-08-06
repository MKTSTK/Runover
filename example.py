from inside_market import *
from hello_market_maker import *
import pandas as pd

trades = pd.read_csv("zfu5.csv", index_col = 0)
trades.index = pd.to_datetime(trades.index)

prices = trades.Price.values.tolist()

hmm = hello_market_maker(100,1,5)

