"""Database CRUD demonstration script.

This script demonstrates full lifecycle operations (Create, Read, Update,
Delete) for StockQuote entities and shows how raw ORM data is transformed
into a pandas-based analytical interface using StockQuoteFrame.

It serves as an integration test for:
- Database connection layer
- Repository and service layers
- DataFrame transformation layer
"""

from datetime import date

from work.scripts.db.session import Database
from work.scripts.db.models import StockQuote
from work.scripts.services.stock_quote_service import StockQuoteService
from work.scripts.contracts import StockQuoteFrame


def main():
    """Run full CRUD + DataFrame demonstration pipeline."""

    print("🚀 Starting DB CRUD demo...")

    # ---------------------------
    # INITIALIZATION
    # ---------------------------
    # Create database manager and service layer
    db = Database()
    service = StockQuoteService(db)

    # ---------------------------
    # CREATE
    # ---------------------------
    print("\n[CREATE] Adding sample records...")

    # Create a sample stock quote (simulated trading day)
    quote = StockQuote(
        trade_date=date(2024, 1, 1),
        source="example.com",
        open_price=100.0,
        high_price=110.0,
        low_price=95.0,
        close_price=105.0,
        volume=1000000,
    )

    # Insert record into database
    service.add_quote(quote)

    # ---------------------------
    # READ
    # ---------------------------
    print("\n[READ] Fetching data from database...")

    # Load full dataset as pandas DataFrame
    df = service.get_all_quotes_df()

    print("\nFirst 5 rows of dataset:")
    print(df.head())

    # Wrap DataFrame into typed analytical interface
    frame = StockQuoteFrame(df)

    # ---------------------------
    # DATAFRAME VIEW (ANALYTICS LAYER)
    # ---------------------------
    print("\n[ANALYTICS] Column-level access via StockQuoteFrame:")

    print("\nHigh prices series:")
    print(frame.high_price.head())

    print("\nTrading volume series:")
    print(frame.volume.head())

    print("\nClose prices series:")
    print(frame.close_price.head())

    # ---------------------------
    # UPDATE
    # ---------------------------
    print("\n[UPDATE] Modifying record...")

    # Update in-memory object
    quote.close_price = 120.0

    # Persist update to database
    service.update_quote(quote)

    print("Update completed: close_price changed to 120.0")

    # ---------------------------
    # DELETE
    # ---------------------------
    print("\n[DELETE] Removing record...")

    # Remove record from database
    service.delete_quote(quote)

    print("Record successfully deleted from database")

    # ---------------------------
    # FINISH
    # ---------------------------
    print("\n✅ CRUD + DataFrame demo finished successfully!")


if __name__ == "__main__":
    main()
