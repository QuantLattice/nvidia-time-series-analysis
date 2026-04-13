from sqlalchemy import text

from work.scripts.db.session import Database


def main() -> None:
    db = Database()

    with db.session() as session:
        result = session.execute(text("SELECT 1"))

        value = result.scalar()

        print("Database connection successful ✔")
        print(f"Query result: {value}")


if __name__ == "__main__":
    main()
