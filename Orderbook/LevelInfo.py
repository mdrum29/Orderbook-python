
class LevelInfo:
    def __init__(self, price_: float, quantity_: int):
        self.Price = price_
        self.Qty = quantity_


class Levels:
    bids = []
    asks = []

    def addOrderToLevel(Order):
        side = Order.GetSide()
        if side == 1:
            # is BUY
            Levels.bids.append(Order)

        if side == 2:
            # is SELL
            Levels.asks.append(Order)

class OrderbookLevelInfos:
    bid_levels = []
    ask_levels = []
    def __init__(self, LevelInfos: LevelInfo, isBid):
            if isBid == True:
                self.bid_levels.append(LevelInfos)
            else:
                self.ask_levels.append(LevelInfos)

    def GetBids(self):
        return self.bid_levels

    def GetAsks(self):
        return self.ask_levels

    def GetOrderLevelInfos(self):
        return self