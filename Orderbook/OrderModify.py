
from Orders import *

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