# src/launcher.py
"""
Launcher entry point for packaged builds.
Starts bundled MySQL (if present) before launching the main app.
"""

from __future__ import annotations

import logging
import os
import sys

from app.portable_mysql import PortableMySQL


def _get_app_root() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _configure_logging(app_root: str) -> None:
    log_dir = os.path.join(
        os.environ.get("LOCALAPPDATA") or app_root,
        "AutoGarageManagement",
        "logs",
    )
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "launcher.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        filename=log_path,
    )


def main() -> None:
    app_root = _get_app_root()
    _configure_logging(app_root)

    init_sql = os.path.join(app_root, "database", "init.sql")
    mysql = PortableMySQL(app_root=app_root)
    mysql.start()
    if mysql.is_available():
        mysql.ensure_database(init_sql)
        mysql.apply_env()

    from main import main as app_main
    try:
        app_main()
    finally:
        mysql.stop()


if __name__ == "__main__":
    main()
