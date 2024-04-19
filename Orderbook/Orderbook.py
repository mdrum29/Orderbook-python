from Orderbook import*
from Orders import *
from OrderModify import *
from Trades import *
from LevelInfo import *


class Orderbook:
    orders_ = {}
    bids_ = {}
    asks_ = {}

    bid_level_info = {}
    ask_level_info = {}

    def __init__(self):
        pass

    @classmethod
    def OrderEntry(self, order_: Order,):

        Orderbook.orders_[order_.GetOrderId()] = order_

        if order_.GetSide() == 1: # bid
            if str(order_.GetPrice()) not in Orderbook.bids_:
                Orderbook.bids_[str(order_.GetPrice())] = []

            Orderbook.bids_[str(order_.GetPrice())].append(order_.GetOrderId()) 
            Orderbook.bids_ = dict(sorted(Orderbook.bids_.items(), key=lambda item: float(item[0])))
        
        elif order_.GetSide() == 2: # ask
            if str(order_.GetPrice()) not in Orderbook.asks_:
                Orderbook.asks_[str(order_.GetPrice())] = []

            Orderbook.asks_[str(order_.GetPrice())].append(order_.GetOrderId()) 
            Orderbook.asks_ = dict(sorted(Orderbook.asks_.items(), key=lambda item: float(item[0]), reverse=True))


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
    

    def GetOrderLevelInfo(self):

        for level in Orderbook.bids_.keys():
            bid_qty = 0
            for order in Orderbook.bids_[level]:
                bid_qty += self.orders_[order].GetRemainingQuantity()
           
            bidInfos = LevelInfo(float(level), bid_qty)
            OrderbookLevelInfos(bidInfos, isBid=True)
            

        for level in Orderbook.asks_.keys():
            ask_qty = 0
            for order in Orderbook.asks_[level]:
                ask_qty += self.orders_[order].GetRemainingQuantity()

            askInfos = LevelInfo(float(level), ask_qty)
            OrderbookLevelInfos(askInfos, isBid=False)

        return OrderbookLevelInfos.GetOrderLevelInfos(OrderbookLevelInfos)
                
        