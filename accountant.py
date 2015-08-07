from inside_market import *

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# the accountant class can do neat things like
#
# 1) Tally up the total pnl of your trade
# 2) plot equity curves
# 3) other neat stuff down the road, probably

class accountant():
  def __init__(self, min_tick, tick_value):
    self._trades = []
    self._min_tick = min_tick
    self._tick_value = tick_value

  def push_trades(self, new_trades):
    self._trades.extend(new_trades)

  def get_final_closed_pnl(self):
    # calculates the total pnl of all trades, assuming you are flat
    position = 0.0
    for trade in self._trades:
      if trade[0] == BID:
        position -= trade[1]
      else:
        position += trade[1]
    return (position / self._min_tick) * self._tick_value
    
  def get_final_open_pnl(self, mark_price):
    pos = 0
    position = 0.0
    for trade in self._trades:
      if trade[0] == BID:
        position -= trade[1]
        pos += 1
      else:
        position += trade[1]
        pos -= 1
    margin = -(pos * -mark_price) + position
    return (margin / self._min_tick) * self._tick_value
