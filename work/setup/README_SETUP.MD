# NVIDIA Stock Analyzer - Setup System Documentation

## Overview

The setup system is cross-platform:

- Windows 10 uses `.bat` wrappers.
- macOS uses `.sh` wrappers.
- The real setup logic lives in `work/setup/setup_manager.py`.
- The project can also be controlled from one entry point:
  `work/scripts/main.py`.

The wrappers are intentionally thin. They only move to the project root and
call the Python setup manager.

---

## Requirements

Both Windows and macOS need:

- Python 3
- project dependencies installed from `requirements.txt`
- MySQL server
- MySQL client command available in `PATH` as `mysql`
- `.env` file in the project root

Example `.env`:

```env
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=nvidia_timeseries
```

`MYSQL_DB` is optional. If it is not set, `nvidia_timeseries` is used.

---

## Single Entry Point

From the project root:

```bash
python3 -m work.scripts.main setup
python3 -m work.scripts.main run
python3 -m work.scripts.main reset
```

On Windows, use `python` or `py -3` if `python3` is not available:

```bat
py -3 -m work.scripts.main setup
py -3 -m work.scripts.main run
py -3 -m work.scripts.main reset
```

Available main commands:

```text
run                 check application DB startup
setup               create mysql.cnf, create DB, apply migrations, verify
reset               drop DB and clear generated files
db-config           create work/config/mysql.cnf
db-check            check MySQL connection
db-init             create application database
db-reset            drop application database
clear-files         clear generated output, graphics, and logs
post-install        verify installation state
migrate             apply Alembic migrations
migration-current   show current Alembic revision
migration-new       create a new Alembic migration
migration-down      downgrade Alembic migrations
```

Examples:

```bash
python3 -m work.scripts.main db-check
python3 -m work.scripts.main migration-new add_stock_quotes_table
python3 -m work.scripts.main migration-down -1
python3 -m work.scripts.main reset --yes
```

---

## Windows 10 Wrappers

Run from Command Prompt or PowerShell:

```bat
work\setup\install.bat
work\setup\reset.bat
work\setup\db\create_mysql_config.bat
work\setup\db\check_mysql.bat
work\setup\db\init_db.bat
work\setup\db\reset_db.bat
work\setup\db\apply_migrations.bat
work\setup\db\alembic_upgrade.bat
work\setup\db\alembic_current.bat
work\setup\db\alembic_revision.bat add_stock_quotes_table
work\setup\db\alembic_downgrade.bat -1
work\setup\reset\clear_files.bat
work\setup\install\post_install.bat
```

---

## macOS Wrappers

Run from Terminal:

```bash
./work/setup/install.sh
./work/setup/reset.sh
./work/setup/db/create_mysql_config.sh
./work/setup/db/check_mysql.sh
./work/setup/db/init_db.sh
./work/setup/db/reset_db.sh
./work/setup/db/alembic_upgrade.sh
./work/setup/db/alembic_current.sh
./work/setup/db/alembic_revision.sh add_stock_quotes_table
./work/setup/db/alembic_downgrade.sh -1
./work/setup/reset/clear_files.sh
./work/setup/install/post_install.sh
```

---

## Install Flow

`setup` / `install` performs:

1. Generate `work/config/mysql.cnf` from `.env`.
2. Check MySQL connection.
3. Create the application database.
4. Apply Alembic migrations.
5. Verify project and database state.

---

## Reset Flow

`reset` performs:

1. Ask for confirmation unless `--yes` is used.
2. Generate `work/config/mysql.cnf` from `.env`.
3. Drop the application database.
4. Clear generated files from:
   - `work/output`
   - `work/graphics`
   - `work/logs`

This operation removes application data from the configured database.
