from LevelInfo import *

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


OrderPointer = {} # keys are order ids, values are order objects
OrderPointers = [] # index of order instances
