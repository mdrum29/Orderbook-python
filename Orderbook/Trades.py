# trade objects
class TradeInfo:
    def __init__(self, OrderId: int, Price: float, Quantity: int):
        self.orderId_ = OrderId
        self.price_ = Price
        self.quantity_ = Quantity

class Trade:
    def __init__(self, BidTradeInfo: TradeInfo, AskTradeInfo: TradeInfo):
        self.bidTrade = BidTradeInfo,
        self.askTrade = AskTradeInfo,

    def GetBidTrade(self):
        return self.bidTrade
    
    def GetAskTrade(self):
        return self.askTrade

Trades = [] # holds trade objects