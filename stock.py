import logging
from datetime import datetime, timedelta
from functools import reduce
from typing import Optional


class Stock:

    def __init__(self, stock_symbol: str, dividend_type: str, last_dividend: int,
                 fixed_dividend: Optional[str], par_value: int):
        """
        Initialize a Stock object.

        Args:
            stock_symbol (str): Symbol of the stock.
            dividend_type (str): Type of dividend ('Common' or 'Preferred').
            last_dividend (int): Last dividend value.
            fixed_dividend (str, optional): Fixed dividend value for preferred stock (percentage).
            par_value (int): Par value of the stock.

        Raises:
            ValueError: If an invalid dividend type is provided.
        """
        if dividend_type not in ['Common', 'Preferred']:
            raise ValueError("Invalid stock type. Must be 'Common' or 'Preferred'.")
        logging.info("Stock initialization")

        self.stock_symbol = stock_symbol
        self.dividend_type = dividend_type
        self.last_dividend = last_dividend
        self.fixed_dividend = (
            int(fixed_dividend.replace("%", "")) / 100 if dividend_type == 'Preferred' else None
        )
        self.par_value = par_value
        self.trades = []

    def calculate_dividend_yield(self, price: int) -> float:
        """
        Calculate the dividend yield.

        Args:
            price (int): Current price of the stock.

        Returns:
            float: Calculated dividend yield
        """
        if self.dividend_type == 'Common':
            return round(self.last_dividend / price, 2)
        return round(self.fixed_dividend * self.par_value / price, 2)

    def calculate_pe_ratio(self, price: int) -> Optional[float]:
        """
        Calculate the P/E ratio.

        Args:
            price (int): Current price of the stock.

        Returns:
            float or None: Calculated P/E ratio or None if dividend yield is not positive.
        """
        dividend_yield = self.calculate_dividend_yield(price)
        if dividend_yield <= 0:
            return None
        return round(price / dividend_yield, 2)

    def record_trade(self, timestamp: datetime, quantity: int, indicator: str, price: int) -> None:
        """
        Record a trade.

        Args:
            timestamp (datetime): Timestamp of the trade.
            quantity (int): Quantity of shares traded.
            indicator (str): Indicator for the trade ('buy' or 'sell').
            price (float): Price per share.

        Raises:
            ValueError: If an invalid indicator, quantity, or price is provided.
        """
        if indicator not in ['buy', 'sell']:
            raise ValueError("Invalid indicator. Must be 'buy' or 'sell'.")

        if quantity <= 0 or price <= 0:
            raise ValueError("Quantity and price must be positive values.")

        self.trades.append({
            "stock_symbol": self.stock_symbol,
            "timestamp": timestamp,
            "quantity": quantity,
            "indicator": indicator,
            "price": price
        })

    def calculate_vm_stock_price(self) -> Optional[float]:
        """
        Calculate the volume-weighted stock price.

        Returns:
            float or None: Calculated volume-weighted stock price or None if no relevant trades.
        """
        fifteen_minutes_ago = datetime.now() - timedelta(minutes=15)
        relevant_trades = [trade for trade in self.trades if trade['timestamp'] >= fifteen_minutes_ago]

        if not relevant_trades:
            logging.debug("No relevant trades found")
            return None

        trades_price = reduce(lambda total, trade: total + trade['price'] * trade['quantity'], relevant_trades, 0)
        shares_count = reduce(lambda total, x: total + x['quantity'], relevant_trades, 0)

        return round(trades_price / shares_count, 2)
