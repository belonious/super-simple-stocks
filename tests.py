import unittest
from datetime import datetime, timedelta

from StockMarket import StockMarket
from stock import Stock


class TestStockClass(unittest.TestCase):

    def setUp(self):
        # Create a sample Stock object for testing
        self.stock = Stock(
            stock_symbol="POP",
            dividend_type="Common",
            last_dividend=2,
            fixed_dividend=None,
            par_value=100
        )

    def test_calculate_dividend_yield_common(self):
        self.assertEqual(self.stock.calculate_dividend_yield(20), 0.1)

    def test_calculate_dividend_yield_preferred(self):
        self.stock.dividend_type = "Preferred"
        self.stock.fixed_dividend = 5
        self.assertEqual(self.stock.calculate_dividend_yield(40), 12.5)

    def test_calculate_pe_ratio_common(self):
        self.assertEqual(self.stock.calculate_pe_ratio(20), 200)

    def test_calculate_pe_ratio_preferred(self):
        self.stock.dividend_type = "Preferred"
        self.stock.fixed_dividend = 5
        self.assertEqual(self.stock.calculate_pe_ratio(40), 3.2)

    def test_record_trade(self):
        timestamp = datetime.now()
        self.stock.record_trade(timestamp, 5, "sell", 30)
        self.assertEqual(len(self.stock.trades), 1)

    def test_calculate_vm_stock_price(self):
        timestamp = datetime.now()
        # Record a buy trade within the last 15 minutes
        self.stock.record_trade(timestamp - timedelta(minutes=10), 10, "buy", 20)
        # Record a sell trade within the last 15 minutes
        self.stock.record_trade(timestamp - timedelta(minutes=5), 5, "sell", 25)
        # Record a sell trade happened more than 15 minutes ago
        self.stock.record_trade(timestamp - timedelta(minutes=55), 5, "sell", 25)
        self.assertEqual(self.stock.calculate_vm_stock_price(), 21.67)

    def test_calculate_vm_stock_price_no_trades(self):
        # No trades recorded, should return None
        self.assertIsNone(self.stock.calculate_vm_stock_price())

    def test_invalid_stock_type(self):
        with self.assertRaises(ValueError):
            Stock("CIZ", "InvalidType", 2, None, 100)

    def test_invalid_indicator(self):
        timestamp = datetime.now()
        with self.assertRaises(ValueError):
            self.stock.record_trade(timestamp, 10, "invalid", 25)

    def test_invalid_quantity(self):
        timestamp = datetime.now()
        with self.assertRaises(ValueError):
            self.stock.record_trade(timestamp, -5, "buy", 25)

    def test_invalid_price(self):
        timestamp = datetime.now()
        with self.assertRaises(ValueError):
            self.stock.record_trade(timestamp, 5, "sell", 0)


class TestStockMarket(unittest.TestCase):

    def setUp(self):
        self.stock_market = StockMarket({
            "POP": Stock("POP", "Common", 2, None, 10),
            "CIZ": Stock("CIZ", "Preferred", 4, "5%", 20),
        })

    def test_get_stock(self):
        stock = self.stock_market.get_stock("POP")
        self.assertIsNotNone(stock)
        self.assertEqual(stock.stock_symbol, "POP")

    def test_calculate_gbce_all_share_index_valid(self):
        timestamp = datetime.now()

        self.stock_market.get_stock("POP").record_trade(timestamp, 3, "buy", 3)
        self.stock_market.get_stock("CIZ").record_trade(timestamp, 3, "sell", 3)
        self.stock_market.get_stock("CIZ").record_trade(timestamp, 3, "sell", 3)

        gbce_index = self.stock_market.calculate_gbce_all_share_index()
        self.assertEqual(gbce_index, 3)

    def test_calculate_gbce_all_share_index_no_trades(self):
        gbce_index = self.stock_market.calculate_gbce_all_share_index()
        self.assertIsNone(gbce_index)


if __name__ == '__main__':
    unittest.main()
