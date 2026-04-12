"""Application entry point."""
from sqlalchemy import text

from work.scripts.db.session import SessionLocal


def main() -> None:
    session = SessionLocal()

    try:
        session.execute(text("SELECT 1"))
        print("Database connection established successfully.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
