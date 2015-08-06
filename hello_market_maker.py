class hello_market_maker():
  def __init__(self, anchor_price, tick_increment, max_pos):
    self.anchor_price = anchor_price
    self.tick_increment = tick_increment
    self.position = 0
    self.upper_bound = anchor_price + ((max_pos + 1) * tick_increment)
    self.lower_bound = anchor_price - ((max_pos + 1) * tick_increment)
    self.max_pos = max_pos
    self.mkt = inside_market(anchor_price - tick_increment, anchor_price + tick_increment)

  def on_bid_fill(self):
    # modify current bid and ask down 1 tick_increment
    #self.mkt.shift(-self.tick_increment)
    self.position += 1
    price = self.mkt.bid.price
    if self.position < self.max_pos:
      self.mkt.shift(-self.tick_increment)
    else:
      self.mkt.exit(BID, self.tick_increment)
    return "BID_FILL @ ", price

  def on_ask_fill(self):
    # modify current bid and ask up 1 tick_increment
    #self.mkt.shift(-self.tick_increment)
    self.position -= 1
    price = self.mkt.ask.price
    if self.position > -self.max_pos:
      self.mkt.shift(self.tick_increment)
    else:
      self.mkt.exit(ASK, self.tick_increment)
    return "ASK_FILL @ ", price

  def evaluate(self, trade_price):
    fill, price = self.mkt.evaluate(trade_price)
    self.adjust_bounds(trade_price)
    if fill == BID:
      self.on_bid_fill()
    elif fill == ASK:
      self.on_ask_fill()
    else:
      filler = 0
    return fill, price

  def adjust_bounds(self, trade_price):
    if trade_price > self.upper_bound:
      self.mkt.shift(self.tick_increment)
      self.upper_bound += self.tick_increment
      self.lower_bound += self.tick_increment
      print "ADJUSTING UP"
    elif trade_price < self.lower_bound:
      self.mkt.shift(-self.tick_increment)
      self.upper_bound -= self.tick_increment
      self.lower_bound -= self.tick_increment
      print "ADJUSTING DOWN"


