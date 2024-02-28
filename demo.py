import logging
from datetime import datetime, timedelta
from StockMarket import StockMarket
from data import SAMPLE_DATA
from stock import Stock

logging.basicConfig(level=logging.INFO)


def init():
    """
    Load data to StockMarket
    """
    stocks = {}
    for stock in SAMPLE_DATA:
        stocks[stock['stock_symbol']] = Stock(
            stock.get("stock_symbol"),
            stock.get("type"),
            stock.get("last_dividend"),
            stock.get("fixed_dividend"),
            stock.get("par_value"),
        )
    return StockMarket(stocks)


market = init()
pop = market.get_stock('POP')
logging.info("calculate_dividend_yield : {}".format(pop.par_value))
logging.info("calculate_pe_ratio : {}".format(pop.calculate_dividend_yield(70)))
now = datetime.now()
pop.record_trade(now - timedelta(minutes=12), 13, 'buy', 59)
pop.record_trade(now - timedelta(minutes=19), 32, 'buy', 61)
pop.record_trade(now - timedelta(minutes=200), 3, 'sell', 57)
logging.info("Volume Weighted Stock Price : {}".format(pop.calculate_vm_stock_price()))
logging.info("GBCE All Share Index: {} ".format(market.calculate_gbce_all_share_index()))
