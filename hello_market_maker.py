import pandas as pd
import numpy as np

from inside_market import *

class hello_market_maker():
  def __init__(self, anchor_price, tick_increment, max_pos):
    self.anchor_price = anchor_price
    self.anchor_price_t = anchor_price
    self.vertical_shift = 0
    self.tick_increment = tick_increment
    self.position = 0
    self.bid_exit_bool = False # In production these would be set to True that way the
    self.ask_exit_bool = False # strategy cannot be on inside mkt without human intervention
    self.exit_buffer = 1000 * tick_increment 
    self.upper_bound = anchor_price + ((max_pos + 1) * tick_increment)
    self.lower_bound = anchor_price - ((max_pos + 1) * tick_increment)
    self.status = DEFAULT
    self.max_pos = max_pos
    self.trades = []
    self.__init_market__()

  def __init_market__(self):
    bid, ask = self.__reprice__()
    self.mkt = inside_market(bid, ask)

  def __reprice__(self):
    inside_bid_price = (self.anchor_price + (self.vertical_shift * self.tick_increment)) - \
                       ((self.position + 1) * self.tick_increment) - \
                       (self.bid_exit_bool * self.exit_buffer)
    inside_ask_price = (self.anchor_price + (self.vertical_shift * self.tick_increment)) - \
                       ((self.position - 1) * self.tick_increment) + \
                       (self.ask_exit_bool * self.exit_buffer)
    return inside_bid_price, inside_ask_price

  def check_boundaries(self, trade_price):
    if trade_price > self.upper_bound:
      print "SHIFTING UP", trade_price
      return 1
    elif trade_price < self.lower_bound:
      print "SHIFTING DN", trade_price
      return -1
    else:
      return 0

  def update_market(self):
    bid, ask = self.__reprice__()
    self.mkt.bid.price = bid
    self.mkt.ask.price = ask

  def reset_boundaries(self):
    AP_t = (self.anchor_price + (self.vertical_shift * self.tick_increment))
    self.upper_bound = AP_t + (self.max_pos * self.tick_increment)
    self.lower_bound = AP_t - (self.max_pos * self.tick_increment)

  def evaluate(self, trade_price):
    fill, price = self.mkt.evaluate(trade_price)
    #print fill, price
    # did we get filled?
    if fill != None:
      # YES
      if fill == BID:
        self.position += 1
        price = self.mkt.bid.price
        self.trades.append((BID, price))
      else:
        self.position -= 1
        price = self.mkt.ask.price
        self.trades.append((ASK, price))
      # are we over our max position?
      if abs(self.position) < self.max_pos:
        # NO
        # reset exit bools
        self.bid_exit_bool = False
        self.ask_exit_bool = False
        # are we out of bounds?
        cb = self.check_boundaries(price)
        if cb == 0:
          # NO
          filler = 0
        elif cb == 1:
          # YES
          # we've breached the upper boundary, shift up 1 increment
          self.vertical_shift += 1
          self.reset_boundaries()
        else:
          # YES
          # we've breached the lower boundary, shift dn 1 increment
          self.vertical_shift -= 1
          self.reset_boundaries()
      else: 
        # YES
        # enter exit mode
        if self.position >= self.max_pos:
          self.bid_exit_bool = True
        elif self.position <= -self.max_pos:
          self.ask_exit_bool = True
        # are we out of bounds
        cb = self.check_boundaries(price)
        if cb == 0:
          # NO
          filler = 0
        elif cb == 1:
          # YES
          # we've breached the upper boundary, shift up 1 increment
          self.vertical_shift += 1
          self.reset_boundaries()
        else:
          # YES
          # we've breached the lower boundary, shift dn 1 increment
          self.vertical_shift -= 1
          self.reset_boundaries()
    else:
      # NO
      cb = self.check_boundaries(trade_price)
      if cb == 0:
        # NO
        filler = 0
      elif cb == 1:
        # YES
        # we've breached the upper boundary, shift up 1 increment
        self.vertical_shift += 1
        self.reset_boundaries()
      else:
        # YES
        # we've breached the lower boundary, shift dn 1 increment
        self.vertical_shift -= 1
        self.reset_boundaries()
    #print cb
    self.update_market()
    return fill, price
