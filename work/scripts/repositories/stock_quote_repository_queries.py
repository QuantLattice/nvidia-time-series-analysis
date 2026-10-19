"""Query mixin for StockQuote read operations.

Provides read-only database access methods as a mixin class.
The concrete repository must supply ``self.session`` (SQLAlchemy
Session) before any method is called.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

from datetime import date
from typing import Optional, List, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from work.scripts.db.models import StockQuote


class StockQuoteRepositoryQueryMixin:
    """Read-only query methods for StockQuote entities.

    Relies on ``self.session`` provided by the concrete class.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    session: Session

    def count_all(self) -> int:
        """Return total number of stock quote records.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return self.session.query(StockQuote).count()

    def get_page(
        self,
        offset: int,
        limit: int,
        sort_col: str = 'trade_date',
        sort_desc: bool = False,
    ) -> List[StockQuote]:
        """Retrieve a sorted page of stock quotes.

        Parameters
        ----------
        offset : int
            Number of rows to skip.
        limit : int
            Maximum number of rows to return.
        sort_col : str, optional
            Column name to sort by. Defaults to 'trade_date'.
        sort_desc : bool, optional
            Sort descending if True. Defaults to False.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        col = getattr(StockQuote, sort_col, StockQuote.trade_date)
        order = col.desc() if sort_desc else col.asc()
        return (
            self.session.query(StockQuote)
            .order_by(order)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_by_id(self, quote_id: int) -> Optional[StockQuote]:
        """Retrieve a stock quote by its primary key.

        Parameters
        ----------
        quote_id : int
            Identifier of the stock quote.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return self.session.get(StockQuote, quote_id)

    def get_all(self) -> List[StockQuote]:
        """Retrieve all stock quote records.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return self.session.query(StockQuote).all()

    def get_by_date_range(
        self,
        start_date: date,
        end_date: date,
    ) -> List[StockQuote]:
        """Retrieve stock quotes within a date range (inclusive).

        Parameters
        ----------
        start_date : date
            Start of the date range (inclusive).
        end_date : date
            End of the date range (inclusive).

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return (
            self.session.query(StockQuote)
            .filter(
                StockQuote.trade_date.between(start_date, end_date)
            )
            .order_by(StockQuote.trade_date.asc())
            .all()
        )

    def get_date_range(
        self,
    ) -> Tuple[Optional[date], Optional[date]]:
        """Return (min_date, max_date) of all stored quotes.

        Returns (None, None) if no records exist.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        min_date, max_date = self.session.query(
            func.min(StockQuote.trade_date),
            func.max(StockQuote.trade_date),
        ).one()
        return min_date, max_date
