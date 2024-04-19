from Orderbook import*
from Orders import *
from OrderModify import *
from Trades import *
from LevelInfo import *

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


if __name__ == "__main__":

    obook = Orderbook()
    for ord in all_orders:
        obook.OrderEntry(ord)


    obook.MatchOrders()
    levs = obook.GetOrderLevelInfo()
    print(" Total Trades: ", len(Trades))
    for trade in Trades:
        ask = trade.GetAskTrade()[0]
        bid = trade.GetBidTrade()[0]

        print("--------------------------------------------------------------------")
        print("Order #", ask.orderId_, " matched against Order #", bid.orderId_, " price ", ask.price_, " size ", ask.quantity_)


    print()