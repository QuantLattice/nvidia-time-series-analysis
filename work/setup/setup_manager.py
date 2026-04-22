"""Cross-platform setup and maintenance commands.

This module replaces OS-specific setup logic with Python code that runs on
Windows and macOS. Small ``.bat`` and ``.sh`` scripts delegate to this module.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = PROJECT_ROOT / "work"
SETUP_DIR = WORK_DIR / "setup"
CONFIG_DIR = WORK_DIR / "config"
MYSQL_CNF = CONFIG_DIR / "mysql.cnf"
ENV_FILE = PROJECT_ROOT / ".env"

LOG_INFO = "[INFO]"
LOG_SUCCESS = "[SUCCESS]"
LOG_WARNING = "[WARNING]"
LOG_ERROR = "[ERROR]"
LOG_STEP = "[STEP]"
LOG_DONE = "[DONE]"


class SetupError(RuntimeError):
    """Error raised by setup automation commands."""


def create_mysql_config() -> None:
    """Create a MySQL client config from the project ``.env`` file."""

    if not ENV_FILE.exists():
        raise SetupError(f".env not found at {ENV_FILE}")

    env = _load_env_file(ENV_FILE)
    mysql_user = env.get("MYSQL_USER")
    mysql_password = env.get("MYSQL_PASSWORD", "")
    mysql_host = env.get("MYSQL_HOST", "localhost")
    mysql_port = env.get("MYSQL_PORT", "3306")

    if not mysql_user:
        raise SetupError("MYSQL_USER is required in .env")

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    print(f"{LOG_INFO} Creating MySQL config...")
    MYSQL_CNF.write_text(
        "\n".join(
            [
                "[client]",
                f"user={mysql_user}",
                f"password={mysql_password}",
                f"host={mysql_host}",
                f"port={mysql_port}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    try:
        MYSQL_CNF.chmod(0o600)
    except OSError:
        pass

    print(f"{LOG_SUCCESS} MySQL config created: {MYSQL_CNF}")


def check_mysql() -> None:
    """Validate that MySQL is reachable with the generated config."""

    _ensure_mysql_config()
    print(f"{LOG_INFO} Checking MySQL connection...")
    _run_mysql(["-s", "-N", "-e", "SELECT 1;"])
    print(f"{LOG_SUCCESS} MySQL connection OK")


def init_db() -> None:
    """Create the application database if it does not exist."""

    _ensure_mysql_config()
    db_name = _get_database_name()
    sql = (
        f"CREATE DATABASE IF NOT EXISTS {_quote_identifier(db_name)} "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )

    print(f"{LOG_INFO} Creating MySQL database...")
    _run_mysql(["-e", sql])
    print(f"{LOG_SUCCESS} Database created successfully")


def reset_db() -> None:
    """Drop the application database if it exists."""

    _ensure_mysql_config()
    db_name = _get_database_name()
    sql = f"DROP DATABASE IF EXISTS {_quote_identifier(db_name)};"

    print(f"{LOG_INFO} Dropping MySQL database...")
    _run_mysql(["-e", sql])
    print(f"{LOG_SUCCESS} Database dropped successfully")


def clear_files() -> None:
    """Clear generated output, graphics, and log files."""

    print(f"{LOG_INFO} Clearing generated files...")
    for relative_dir in ("output", "graphics", "logs"):
        directory = WORK_DIR / relative_dir
        directory.mkdir(parents=True, exist_ok=True)
        _clear_directory(directory)

    print(f"{LOG_SUCCESS} Generated files cleared")


def post_install() -> None:
    """Run post-installation verification checks."""

    print(f"{LOG_INFO} Verifying installation state...")
    _ensure_mysql_config()

    for relative_dir in ("config", "scripts", "setup"):
        path = WORK_DIR / relative_dir
        if not path.exists():
            raise SetupError(f"Required project path is missing: {path}")
        print(f"{LOG_INFO} - {relative_dir} exists")

    db_name = _get_database_name()
    sql = f"SHOW DATABASES LIKE '{_quote_string(db_name)}';"
    result = _run_mysql(["-s", "-N", "-e", sql], capture_output=True)
    if db_name not in result.stdout:
        raise SetupError(f"Database was not found: {db_name}")
    print(f"{LOG_INFO} - database exists: {db_name}")

    print(f"{LOG_SUCCESS} Verification completed")


def alembic_upgrade() -> None:
    """Apply all Alembic migrations."""

    print(f"{LOG_STEP} Upgrading database to HEAD...")
    _run_alembic(["upgrade", "head"])
    print(f"{LOG_DONE} Database successfully upgraded")


def alembic_current() -> None:
    """Print the current Alembic revision."""

    print(f"{LOG_STEP} Checking current DB revision...")
    _run_alembic(["current"])


def alembic_revision(message: str) -> None:
    """Create a new Alembic revision with autogeneration."""

    if not message.strip():
        raise SetupError("Migration message is required")

    print(f"{LOG_STEP} Generating migration...")
    print(f"{LOG_INFO} Message: {message}")
    _run_alembic(["revision", "--autogenerate", "-m", message])
    print(f"{LOG_DONE} Migration created successfully")


def alembic_downgrade(revision: str | None = None) -> None:
    """Downgrade the database to a revision or one revision back."""

    target_revision = revision or "-1"
    print(f"{LOG_STEP} Downgrading to revision: {target_revision}")
    _run_alembic(["downgrade", target_revision])
    print(f"{LOG_DONE} Downgrade completed")


def install() -> None:
    """Run the full setup flow."""

    print("======================================")
    print("  NVIDIA Stock Analyzer Setup")
    print("======================================")
    print()

    print(f"{LOG_STEP} Step 1: Preparing MySQL config...")
    create_mysql_config()
    print()

    print(f"{LOG_STEP} Step 2: Checking MySQL connection...")
    check_mysql()
    print()

    print(f"{LOG_STEP} Step 3: Initializing database...")
    init_db()
    print()

    print(f"{LOG_STEP} Step 4: Applying database migrations...")
    alembic_upgrade()
    print()

    print(f"{LOG_STEP} Step 5: Final verification...")
    post_install()
    print()

    print(f"{LOG_DONE} Setup completed successfully!")
    print(f"{LOG_INFO} You can now run: python -m work.scripts.main run")


def reset(confirm: bool = False) -> None:
    """Run the full reset flow."""

    print("======================================")
    print("  NVIDIA Project Reset Tool")
    print("======================================")
    print()
    print(f"{LOG_WARNING} This will reset all project data!")
    print()

    if not confirm:
        user_input = input("Type YES to continue: ")
        if user_input.upper() != "YES":
            print(f"{LOG_INFO} Reset cancelled by user")
            return

    print()
    print(f"{LOG_STEP} Preparing MySQL config...")
    create_mysql_config()
    print()

    print(f"{LOG_STEP} Dropping database...")
    reset_db()
    print()

    print(f"{LOG_STEP} Clearing generated files...")
    clear_files()
    print()

    print(f"{LOG_DONE} Reset completed successfully")


def run_cli(argv: list[str] | None = None) -> int:
    """Run setup automation from command-line arguments."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        _dispatch(args)
    except (
        SetupError,
        FileNotFoundError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"{LOG_ERROR} {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(f"{LOG_INFO} Cancelled by user", file=sys.stderr)
        return 130

    return 0


def _build_parser() -> argparse.ArgumentParser:
    """Build the setup command parser."""

    parser = argparse.ArgumentParser(
        prog="setup_manager",
        description="Cross-platform setup commands for the project.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("install", help="run full project setup")
    subparsers.add_parser("create-mysql-config", help="create mysql.cnf")
    subparsers.add_parser("check-mysql", help="check MySQL connection")
    subparsers.add_parser("init-db", help="create the application database")
    subparsers.add_parser("reset-db", help="drop the application database")
    subparsers.add_parser("clear-files", help="clear generated files")
    subparsers.add_parser("post-install", help="verify installation state")
    subparsers.add_parser("alembic-upgrade", help="apply migrations")
    subparsers.add_parser("alembic-current", help="show current revision")

    revision_parser = subparsers.add_parser(
        "alembic-revision",
        help="create an autogenerate migration",
    )
    revision_parser.add_argument("message", nargs="+")

    downgrade_parser = subparsers.add_parser(
        "alembic-downgrade",
        help="downgrade migrations",
    )
    downgrade_parser.add_argument("revision", nargs="?")

    reset_parser = subparsers.add_parser("reset", help="run full reset")
    reset_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="skip interactive reset confirmation",
    )

    return parser


def _dispatch(args: argparse.Namespace) -> None:
    """Dispatch parsed CLI arguments to command functions."""

    command = args.command
    if command == "install":
        install()
    elif command == "create-mysql-config":
        create_mysql_config()
    elif command == "check-mysql":
        check_mysql()
    elif command == "init-db":
        init_db()
    elif command == "reset-db":
        reset_db()
    elif command == "clear-files":
        clear_files()
    elif command == "post-install":
        post_install()
    elif command == "alembic-upgrade":
        alembic_upgrade()
    elif command == "alembic-current":
        alembic_current()
    elif command == "alembic-revision":
        alembic_revision(" ".join(args.message))
    elif command == "alembic-downgrade":
        alembic_downgrade(args.revision)
    elif command == "reset":
        reset(confirm=args.yes)
    else:
        raise SetupError(f"Unknown command: {command}")


def _load_env_file(env_path: Path) -> dict[str, str]:
    """Load simple KEY=VALUE pairs from a dotenv file."""

    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            values[key] = value

    return values


def _get_database_name() -> str:
    """Return the configured application database name."""

    if ENV_FILE.exists():
        env = _load_env_file(ENV_FILE)
    else:
        env = {}

    return env.get("MYSQL_DB") or os.getenv("MYSQL_DB") or "nvidia_timeseries"


def _ensure_mysql_config() -> None:
    """Ensure the generated MySQL client config exists."""

    if not MYSQL_CNF.exists():
        raise SetupError(
            "MySQL config not found. Run create-mysql-config first."
        )


def _run_mysql(
    args: list[str],
    *,
    capture_output: bool = False
) -> subprocess.CompletedProcess[str]:
    """Run the MySQL CLI with the generated config file."""

    mysql_executable = shutil.which("mysql")
    if mysql_executable is None:
        raise SetupError(
            "mysql command was not found. Install MySQL client and add it "
            "to PATH."
        )

    command = [
        mysql_executable,
        f"--defaults-extra-file={MYSQL_CNF}",
        *args,
    ]
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=capture_output,
        text=True,
    )


def _run_alembic(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run Alembic through the current Python interpreter."""

    command = [sys.executable, "-m", "alembic", *args]
    return subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def _clear_directory(directory: Path) -> None:
    """Remove all children from a directory without deleting the directory."""

    for child in directory.iterdir():
        if child.name == ".gitkeep":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def _quote_identifier(identifier: str) -> str:
    """Quote a MySQL identifier with backticks."""

    return f"`{identifier.replace('`', '``')}`"


def _quote_string(value: str) -> str:
    """Escape a MySQL string literal body."""

    return value.replace("\\", "\\\\").replace("'", "\\'")


if __name__ == "__main__":
    raise SystemExit(run_cli())
