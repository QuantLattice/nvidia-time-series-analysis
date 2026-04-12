"""Creates session for connecting to DB."""
import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def load_config() -> dict:
    project_root = Path(__file__).resolve().parents[3]
    config_path = project_root / "work" / "config" / "app_config.json"

    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_db_url() -> str:
    config = load_config()

    db_config = config["database"]

    db_engine = db_config["engine"]
    host = db_config["host"]
    port = db_config["port"]
    user = db_config["user"]
    password = db_config["password"]
    database = db_config["database"]

    if db_engine != "mysql":
        raise ValueError(f"Unsupported database engine: {db_engine}")

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"


DATABASE_URL = build_db_url()

engine = create_engine(
    url=DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
