"""Application startup actions."""

from sqlalchemy import text

from work.scripts.db.session import Database


def run_application() -> None:
    """Run the current application startup check."""

    db = Database()
    with db.session() as session:
        result = session.execute(text("SELECT 1"))
        value = result.scalar()

    print("Database connection successful")
    print(f"Query result: {value}")
