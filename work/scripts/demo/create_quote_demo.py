"""Create one stock quote through the controller layer.

Run from the project root:

    python3 -m work.scripts.demo.create_quote_demo
"""

from work.scripts.controllers import StockQuoteController
from work.scripts.db.session import Database
from work.scripts.services import StockQuoteService


def main() -> None:
    """Create a sample stock quote and print the controller result."""

    db = Database()
    service = StockQuoteService(db)
    controller = StockQuoteController(service)

    result = controller.create_quote(
        {
            "trade_date": "2026-04-21",
            "source": "https://example.com/nvda/2026-04-21",
            "open_price": 850.50,
            "high_price": 875.00,
            "low_price": 842.10,
            "close_price": 870.25,
            "adj_close_price": 870.25,
            "volume": 35000000,
        }
    )

    print(result)


if __name__ == "__main__":
    main()
