import random
import time
from typing import List

from pb2.stock_exchange_pb2 import StockData, Offer, Currency


class MockDataGenerator:
    @classmethod
    def generate_offers(cls, num_offers=3) -> List[Offer]:
        offers = []
        for _ in range(num_offers):
            offer = Offer(
                price=random.uniform(0.5, 1000),
                quantity=random.randint(1, 100)
            )
            offers.append(offer)
        return offers

    @classmethod
    def get_stock_data(cls, symbol) -> StockData:
        best_bid_offers = cls.generate_offers()
        best_ask_offers = cls.generate_offers()

        return StockData(
            symbol=symbol,
            company_name="Company Name",
            price=random.uniform(1, 1000),
            pct_change=random.uniform(-10, 10),
            volume=random.randint(1, 1000),
            timestamp=int(time.time()),
            best_bid_offers=best_bid_offers,
            best_ask_offers=best_ask_offers,
            currency=Currency.USD
        )

    @classmethod
    def get_available_symbols(cls):
        return ["AAPL", "AMZN", "GOOG", "FB", "TSLA", "MSFT", "NVDA", "PYPL", "ADBE", "NFLX"]
