"""Command-line interface for application and setup commands."""

from __future__ import annotations

import argparse
import subprocess
import sys

from work.scripts.app_runner import run_application
from work.setup import setup_manager


def main(argv: list[str] | None = None) -> int:
    """Run the project CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        dispatch(args)
    except (
        setup_manager.SetupError,
        FileNotFoundError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"{setup_manager.LOG_ERROR} {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(f"{setup_manager.LOG_INFO} Cancelled by user", file=sys.stderr)
        return 130

    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the project command parser."""

    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Single entry point for app startup and setup commands.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("run", help="run application startup check")
    subparsers.add_parser("setup", help="create DB config, DB, and migrations")

    reset_parser = subparsers.add_parser("reset", help="reset DB and outputs")
    reset_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="skip interactive reset confirmation",
    )

    subparsers.add_parser("db-config", help="create MySQL config")
    subparsers.add_parser("db-check", help="check MySQL connection")
    subparsers.add_parser("db-init", help="create application database")
    subparsers.add_parser("db-reset", help="drop application database")
    subparsers.add_parser("clear-files", help="clear generated files")
    subparsers.add_parser("post-install", help="verify installation state")
    subparsers.add_parser("migrate", help="apply Alembic migrations")
    subparsers.add_parser("migration-current", help="show DB revision")

    revision_parser = subparsers.add_parser(
        "migration-new",
        help="create a new Alembic migration",
    )
    revision_parser.add_argument("message", nargs="+")

    downgrade_parser = subparsers.add_parser(
        "migration-down",
        help="downgrade Alembic migrations",
    )
    downgrade_parser.add_argument("revision", nargs="?")

    return parser


def dispatch(args: argparse.Namespace) -> None:
    """Dispatch parsed CLI arguments to project commands."""

    command = args.command or "run"
    commands = {
        "run": run_application,
        "setup": setup_manager.install,
        "db-config": setup_manager.create_mysql_config,
        "db-check": setup_manager.check_mysql,
        "db-init": setup_manager.init_db,
        "db-reset": setup_manager.reset_db,
        "clear-files": setup_manager.clear_files,
        "post-install": setup_manager.post_install,
        "migrate": setup_manager.alembic_upgrade,
        "migration-current": setup_manager.alembic_current,
    }

    if command == "reset":
        setup_manager.reset(confirm=args.yes)
    elif command == "migration-new":
        setup_manager.alembic_revision(" ".join(args.message))
    elif command == "migration-down":
        setup_manager.alembic_downgrade(args.revision)
    elif command in commands:
        commands[command]()
    else:
        raise setup_manager.SetupError(f"Unknown command: {command}")
