from statistics import geometric_mean
import logging


class StockMarket:
    """
        Represents a stock market that manages multiple stocks.

        Attributes:
          stocks (dict): A dictionary where keys are stock symbols and values are Stock objects.
    """
    def __init__(self, stocks):
        """
            Initialize the StockMarket with the provided dictionary of stocks.

            Args:
                stocks (dict):
        """
        logging.info("Stock market initialization")
        self.stocks = stocks

    def calculate_gbce_all_share_index(self):
        """
           Calculate the GBCE (Geometric Mean) All Share Index based on the prices of all trades.

           Returns:
               float or None: The calculated index as a float rounded to two decimal places. Returns None if
               no trades are available.
        """
        logging.info("calculating all shares index")
        prices = [trade['price'] for stock in self.stocks.values() for trade in stock.trades]
        logging.debug(f"total prices {len(prices)}")
        return round(geometric_mean(prices), 2) if len(prices) > 0 else None

    def get_stock(self, stock_symbol):
        """
            Retrieve the Stock object with the given stock symbol from the stock market.

            Args:
                stock_symbol (str): The stock symbol to look up.

            Returns:
                Stock or None
        """
        return self.stocks.get(stock_symbol)
