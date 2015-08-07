import pandas as pd
import numpy as np

# update current state of our bid and ask
# iterate thru each trade and determine if a fill was generated

# id
# price
# qty
# side - bid/ask
# status - live, canceled, rejected

LIVE     = 0
CANCELED = 1
REJECTED = 2
FILLED   = 3
PARTIAL  = 4

BID      = 5
ASK      = 6

MINUS_INF = -9999999
PLUS_INF  =  9999999

# STATUSES

DEFAULT  = 7
EXIT     = 8

# represents a limit order in our inside market
class order():
  id = 0
  def __init__(self, price, qty, side, status):
    self.id = order.id
    order.id += 1
    self.price = price
    self.qty = qty
    self.side = side
    self.status = status

  def cancel(self):
    self.status = CANCELED

  def modify(self, new_price, new_qty = -1):
    self.price = new_price
    if new_qty > 0:
      self.qty = new_qty

  def evaluate(self, trade_price):
    if self.side == BID:
      if trade_price < self.price:
        self.status = FILLED
        return True, self.price
      else:
        return False, trade_price
    else:
      if trade_price > self.price:
        self.status = FILLED
        return True, self.price
      else:
        return False, trade_price
        
class inside_market():
  def __init__(self, bid_price, ask_price):
    if bid_price < ask_price:
      self.bid = order(bid_price, 1, BID, LIVE)
      self.ask = order(ask_price, 1, ASK, LIVE)
      self.status = 1
    else:
      self.status = -1

  def update(self, side, new_price):
    if side == BID:
      if new_price < self.ask.price:
        self.bid.price = new_price
        return True, "MODIFIED ORDER ID = ", self.bid.id
      else:
        return False, "FAILED TO MODIFY ORDER ID = ", self.bid.id, " RESULTING BID WOULD HAVE CROSSED OUR ASK"
    else:
      if new_price > self.bid.price:
        self.ask.price = new_price
        return True, "MODIFIED ORDER ID = ", self.ask.id
      else:
        return False, "FAILED TO MODIFY ORDER ID = ", self.bid.id, " RESULTING ASK WOULD HAVE CROSSED OUR BID"
  
  def evaluate(self, trade_price):
    bid_fill, bid_fill_price = self.bid.evaluate(trade_price)
    ask_fill, ask_fill_price = self.ask.evaluate(trade_price)
    if bid_fill == True:
      return BID, bid_fill_price
    elif ask_fill == True:
      return ASK, ask_fill_price
    else:
      return None, 0.0

  def shift(self, increment):
    self.bid.price += increment
    self.ask.price += increment

  def exit(self, side, increment):
    if side == BID:
      # shift the bid down to minus_inf to not buy anymore
      self.bid.price = MINUS_INF
      self.ask.price -= increment
    else:
      # shift the ask up to plus_inf to not sell anymore
      self.ask.price = PLUS_INF
      self.bid.price += increment
