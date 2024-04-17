class OrderType:
    GoodTillCancel = 1
    FillAndKill = 2


class Side:
    BUY = 1
    SELL = 2


class OrderList:
    orderslist = {}

    @staticmethod
    def GetOrder(OrderId):
        if OrderId in OrderList.orderslist.keys():
            return OrderList.orderslist[OrderId]
        
        else:
            return None
    
    @staticmethod
    def getAllOrders():
        if  len(OrderList.orderslist.keys()) > 0:
            return OrderList.orderslist
        else:
            return None




class Order:
    def __init__(self, OrderType: OrderType, OrderId: int, Side: Side, Price: float, Qty: int):
        self.OrderType = OrderType
        self.OrderId = OrderId
        self.Side = Side

        if Price.is_integer():
            Price = int(Price)

        self.Price = Price
        self.Qty = Qty
        self.initialQty = Qty
        self.remainingQty = Qty
        OrderList.orderslist[OrderId] = self
        Levels.addOrderToLevel(self)

        OrderPointer[OrderId] = self

    def GetOrderId(self):
        return self.OrderId
    
    def GetSide(self):
        return self.Side

    def GetPrice(self):
        return self.Price
    
    def GetOrderType(self):
        return self.OrderType
    
    def GetInitialQuantity(self):
        return self.initialQty
    
    def GetRemainingQuantity(self):
        return self.remainingQty
    
    def GetFilledQuantity(self):
        return self.initialQty - self.remainingQty
    
    def isFilled(self):
        if self.remainingQty == 0:
            return True
        else:
            return False
    
    def Fill(self, quantity: int):
    
        if quantity > self.remainingQty:
            Exception("ERROR Quantity requested is larger than remaining to fill.")
        else:
            self.remainingQty -= quantity


class OrderModify:
    def __init__(self, OrderId: int, Side: Side, Price: float, Qty: int): 
        self.OrderId = OrderId
        self.Side = Side
        self.Price = Price
        self.Qty = Qty
        
    def GetOrderId(self):
        return self.OrderId
    
    def GetSide(self):
        return self.Side

    def GetPrice(self):
        return self.Price
    
    def GetQuantity(self):
        return self.Qty
    
    def ToOrderPointer(self, OrderType: OrderType):
        return Order(OrderType, self.GetOrderId(), self.GetSide(), self.GetPrice(), self.GetQuantity())

# Orderbook objects 
class LevelInfo:
    def __init__(self, price_: float, quantity_: int):
        self.Price = price_
        self.Qty = quantity_

class Levels:
    bids = []
    asks = []

    def addOrderToLevel(Order: Order):
        side = Order.GetSide()
        if side == Side.BUY:
            # is BUY
            Levels.bids.append(Order)

        if side == Side.SELL:
            # is SELL
            Levels.asks.append(Order)

class OrderbookLevelInfos:
    def __init__(self, Levels: Levels):
        self.bids_ = Levels.bids
        self.asks_ = Levels.asks

    def GetBids(self):
        return self.bids_

    def GetAsks(self):
        return self.asks_

OrderPointer = {} # keys are order ids, values are order objects
OrderPointers = [] # index of order instances

class Orderbook:
    orders_ = {}
    bids_ = {}
    asks_ = {}

    def __init__(self):
        pass

    @classmethod
    def OrderEntry(self, order_: Order,):

        Orderbook.orders_[order_.GetOrderId()] = order_

        if order_.GetSide() == 1: # bid
            if str(order_.GetPrice()) not in Orderbook.bids_:
                Orderbook.bids_[str(order_.GetPrice())] = []

            Orderbook.bids_[str(order_.GetPrice())].append(order_.GetOrderId()) 
            Orderbook.bids_ = dict(sorted(Orderbook.bids_.items()))
        
        elif order_.GetSide() == 2: # ask
            if str(order_.GetPrice()) not in Orderbook.asks_:
                Orderbook.asks_[str(order_.GetPrice())] = []

            Orderbook.asks_[str(order_.GetPrice())].append(order_.GetOrderId()) 
            Orderbook.asks_ = dict(sorted(Orderbook.asks_.items(), reverse=True))

    def CanMatch(self, side: Side, price: float): 

        # BUY SIDE
        if side == Side.BUY:
            if not self.asks_:
                return False

            else:
                best_ask = min(map(float, self.asks_.keys()))
                return price >= best_ask
            
        # SELL SIDE
        elif side == Side.SELL:
            if not self.bids_:
                return False
            
            else:
                best_bid = max(map(float, self.bids_.keys()))
                return price <= best_bid
            
    
    def MatchOrders(self):

        while self.asks_ and self.bids_:
            if not self.asks_ or not self.bids_:
                break
            
            best_ask_price = min(map(float, self.asks_.keys()))
            best_bid_price = max(map(float, self.bids_.keys()))

            if best_ask_price.is_integer():
                best_ask_price = int(best_ask_price)
            
            if best_bid_price.is_integer():
                best_bid_price = int(best_bid_price)

            if best_bid_price < best_ask_price:
                break

            bid_pointer = self.bids_[str(best_bid_price)][0] # gets the best bid pointer (location in the OrderPointer list) that was first on the book
            ask_pointer = self.asks_[str(best_ask_price)][0] # gets the best ask  (location in the OrderPointer list) that was first on the book

            bid = OrderPointer[bid_pointer]
            ask = OrderPointer[ask_pointer]

            match_quantity = min(bid.GetRemainingQuantity(), ask.GetRemainingQuantity())

            bid.Fill(match_quantity)
            ask.Fill(match_quantity)

            if bid.isFilled():
                self.bids_[str(best_bid_price)].pop(0)
                self.orders_.pop(bid.GetOrderId()) 

            if ask.isFilled():
                self.asks_[str(best_ask_price)].pop(0)
                self.orders_.pop(ask.GetOrderId()) 

            if not self.bids_[str(best_bid_price)]:
                self.bids_.pop(str(best_bid_price))
            
            if not self.asks_[str(best_ask_price)]:
                self.asks_.pop(str(best_ask_price))

            trade_object = Trade(TradeInfo(bid.GetOrderId(), bid.GetPrice(), match_quantity), TradeInfo(ask.GetOrderId(), ask.GetPrice(), match_quantity), )
            Trades.append(trade_object)
        
        

        if self.bids_:
            firstBid = OrderPointer[self.bids_[str(min(map(float, self.bids_.keys())))][0]]

            if firstBid.GetOrderType() == OrderType.FillAndKill:
                Orderbook.CancelOrder(self, firstBid.GetOrderId())
        
        if self.asks_:
            firstAsk = OrderPointer[self.asks_[str(max(map(float, self.asks_.keys())))][0]]

            if firstAsk.GetOrderType() == OrderType.FillAndKill:
                Orderbook.CancelOrder(self, firstAsk.GetOrderId())

        return Trades

    def AddOrder(self, order: Order):
        # add order to orderbook

        if order.GetOrderId() in self.orders_.keys(): # catching duplicates
            print("Order ID already exists.")
            return

        if order.GetOrderType() == OrderType.FillAndKill and not Orderbook.CanMatch(order.GetSide(), order.GetPrice()):
            print("Could not match FillAndKill order. Order not added to the orderbook")
            return

        # iterator = order
        if order.GetSide() == Side.BUY:
            orders = self.bids_[order.GetPrice()]
            orders.append(order)
            iterator = len(orders) - 1

        elif order.GetSide() == Side.SELL:
            orders = self.asks_[order.GetPrice()]
            orders.append(order)
            iterator = len(orders) - 1

        # add order to the book
        self.orders_[order.GetOrderId()] = Orderbook.OrderEntry(order, iterator)

        # run matches on new order
        Orderbook.MatchOrders()
        return
    
    def CancelOrder(self, OrderId: int):
        if OrderId not in self.orders_.keys():
            print('Did not cancel. Order does not exist.')
            return
        
        order = self.orders_[OrderId]
        self.orders_.pop(OrderId)

        if order.GetSide() == Side.SELL:
            price = str(order.GetPrice())
            orders = self.asks_[price]
            idx = self.asks_[price].index(OrderId)
            orders.pop(idx)

            if not orders:
                self.asks_.pop(price)

        elif order.GetSide() == Side.BUY:
            price = str(order.GetPrice())
            orders = self.bids_[price]
            idx = self.asks_[price].index(OrderId)
            orders.pop(idx)

            if not orders:
                self.bids_.pop(price)

    def ModifyOrder(self, order: Order): 
        if order.GetOrderId() not in self.orders_.keys():
            return

        existingOrder = self.orders_[order.GetOrderId()]  
        Orderbook.CancelOrder(order.GetOrderId())
        return Orderbook.AddOrder(existingOrder)
    
    def Size(self):
        return len(self.orders_)
    
    # def GetOrderInfos():


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

if __name__ == "__main__":

    order1 = Order(OrderType.GoodTillCancel, 100, Side.BUY, 100, 500)
    order2 = Order(OrderType.FillAndKill, 101, Side.SELL, 101.5, 250)
    order3 = Order(OrderType.GoodTillCancel, 102, Side.SELL, 99.8, 800)
    order4 = Order(OrderType.GoodTillCancel, 103, Side.BUY, 100.00, 750)
    order5 = Order(OrderType.GoodTillCancel, 104, Side.SELL, 101.5, 900)
    order6 = Order(OrderType.GoodTillCancel, 105, Side.SELL, 99.8, 1000)
    order7 = Order(OrderType.GoodTillCancel, 106, Side.BUY, 100.00, 1500)
    order8 = Order(OrderType.GoodTillCancel, 107, Side.BUY, 101.5, 100)
    order9 = Order(OrderType.GoodTillCancel, 108, Side.SELL, 99.8, 700)
    order10 = Order(OrderType.GoodTillCancel, 109, Side.BUY, 99.8, 1000)
    order11 = Order(OrderType.GoodTillCancel, 110, Side.SELL, 93.8, 1000)
    order12 = Order(OrderType.GoodTillCancel, 111, Side.BUY, 100.8, 660)
    order13 = Order(OrderType.FillAndKill, 112, Side.BUY, 103.1, 1000)
    order14 = Order(OrderType.FillAndKill, 113, Side.SELL, 96, 2100)
    order15 = Order(OrderType.GoodTillCancel, 114, Side.BUY, 100.8, 500)

    
    order16 = Order(OrderType.GoodTillCancel, 200, Side.SELL, 78.01, 1000)
    order17 = Order(OrderType.FillAndKill, 201, Side.SELL, 103, 300)
    order18 = Order(OrderType.GoodTillCancel, 202, Side.SELL, 88.5, 650)
    order19 = Order(OrderType.GoodTillCancel, 203, Side.BUY, 141.1, 550)
    order20 = Order(OrderType.GoodTillCancel, 204, Side.BUY, 131.1, 100)
    order21 = Order(OrderType.GoodTillCancel, 205, Side.SELL, 107.1, 200)
    order22 = Order(OrderType.GoodTillCancel, 206, Side.BUY, 102.1, 150)
    order23 = Order(OrderType.GoodTillCancel, 207, Side.BUY, 89.1, 2000)
    order24 = Order(OrderType.GoodTillCancel, 208, Side.SELL, 88.7, 600)
    order25 = Order(OrderType.GoodTillCancel, 209, Side.BUY, 100, 500)
    order26 = Order(OrderType.GoodTillCancel, 210, Side.SELL, 88.8, 500)
    order27 = Order(OrderType.GoodTillCancel, 211, Side.BUY, 84.3, 100)
    order28 = Order(OrderType.FillAndKill, 212, Side.BUY, 100, 200)
    order29 = Order(OrderType.FillAndKill, 213, Side.SELL, 94.2, 125)
    order30 = Order(OrderType.GoodTillCancel, 214, Side.BUY, 94.2, 400)

    all_orders = [
        order1, order2, order3, order4, order5, order6, order7, order8, order9, order10,
        order11, order12, order13, order14, order15, order16, order17, order18, order19, order20,
        order21, order22, order23, order24, order25, order26, order27, order28, order29, order30,

                  ]

    obook = Orderbook()
    for ord in all_orders:
        obook.OrderEntry(ord)


    obook.MatchOrders()

    print(" Total Trades: ", len(Trades))
    for trade in Trades:
        ask = trade.GetAskTrade()[0]
        bid = trade.GetBidTrade()[0]

        print("--------------------------------------------------------------------")
        print("Order #", ask.orderId_, " matched against Order #", bid.orderId_, " price ", ask.price_, " size ", ask.quantity_)


    print()