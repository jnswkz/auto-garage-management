# src/app/portable_mysql.py
"""
Portable MySQL bootstrap for bundled deployments.
Starts a bundled MySQL server, initializes data dir, and loads schema/data.
"""

from __future__ import annotations

import atexit
import logging
import os
import socket
import subprocess
import time
from typing import Optional

logger = logging.getLogger(__name__)


class PortableMySQL:
    def __init__(
        self,
        app_root: str,
        app_name: str = "AutoGarageManagement",
        host: str = "127.0.0.1",
        port: int = 3307,
        user: str = "root",
        password: str = "",
        database: str = "garagemanagement",
    ) -> None:
        self.app_root = app_root
        self.app_name = app_name
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self.mysql_root = os.path.join(self.app_root, "mysql")
        self.bin_dir = os.path.join(self.mysql_root, "bin")
        self.mysqld_path = os.path.join(self.bin_dir, "mysqld.exe")
        self.mysql_path = os.path.join(self.bin_dir, "mysql.exe")
        self.mysqladmin_path = os.path.join(self.bin_dir, "mysqladmin.exe")

        local_app_data = os.environ.get("LOCALAPPDATA") or self.app_root
        self.runtime_root = os.path.join(local_app_data, self.app_name, "mysql")
        self.data_dir = os.path.join(self.runtime_root, "data")
        self.log_dir = os.path.join(local_app_data, self.app_name, "logs")
        self.ini_path = os.path.join(self.runtime_root, "my.ini")

        self._process: Optional[subprocess.Popen] = None
        self._started_by_us = False

    def is_available(self) -> bool:
        return os.path.isfile(self.mysqld_path) and os.path.isfile(self.mysql_path)

    def start(self) -> None:
        if not self.is_available():
            logger.info("Portable MySQL not found; skipping bundled MySQL startup.")
            return

        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.runtime_root, exist_ok=True)

        self._write_my_ini()
        self._initialize_data_dir_if_needed()

        if self._is_port_open(self.host, self.port):
            logger.info("MySQL port already open; assuming server is running.")
            return

        args = [
            self.mysqld_path,
            f"--defaults-file={self.ini_path}",
            "--console",
        ]
        self._process = subprocess.Popen(
            args,
            cwd=self.mysql_root,
            creationflags=self._creation_flags(),
        )
        self._started_by_us = True
        atexit.register(self.stop)

        self._wait_for_port(self.host, self.port, timeout=20)
        logger.info("Portable MySQL started on %s:%s", self.host, self.port)

    def ensure_database(self, init_sql_path: str) -> None:
        if not self.is_available():
            return

        if not os.path.isfile(init_sql_path):
            raise FileNotFoundError(f"Init SQL not found: {init_sql_path}")

        self._wait_for_mysql_ready()

        if self._database_exists():
            return

        logger.info("Initializing database from %s", init_sql_path)
        mysql_args = self._mysql_base_args()
        with open(init_sql_path, "rb") as handle:
            self._run_mysql(mysql_args, stdin=handle)

    def apply_env(self) -> None:
        if not self.is_available():
            return

        os.environ.setdefault("DB_HOST", self.host)
        os.environ.setdefault("DB_PORT", str(self.port))
        os.environ.setdefault("DB_USER", self.user)
        os.environ.setdefault("DB_PASSWORD", self.password)
        os.environ.setdefault("DB_NAME", self.database)

    def stop(self) -> None:
        if not self._started_by_us:
            return

        if self._process and self._process.poll() is None:
            if os.path.isfile(self.mysqladmin_path):
                args = [
                    self.mysqladmin_path,
                    "-h",
                    self.host,
                    "-P",
                    str(self.port),
                    "-u",
                    self.user,
                    "shutdown",
                ]
                try:
                    subprocess.run(args, check=True, creationflags=self._creation_flags())
                except subprocess.SubprocessError:
                    logger.exception("mysqladmin shutdown failed; terminating process.")
                    self._process.terminate()
            else:
                self._process.terminate()

            try:
                self._process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._process.kill()

        self._process = None
        self._started_by_us = False

    def _write_my_ini(self) -> None:
        ini = [
            "[mysqld]",
            f"basedir={self._norm_path(self.mysql_root)}",
            f"datadir={self._norm_path(self.data_dir)}",
            f"port={self.port}",
            "bind-address=127.0.0.1",
            "character-set-server=utf8mb4",
            "collation-server=utf8mb4_0900_ai_ci",
            "sql_mode=STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION",
            "",
            "[client]",
            f"host={self.host}",
            f"port={self.port}",
            "user=root",
        ]
        with open(self.ini_path, "w", encoding="ascii") as handle:
            handle.write("\n".join(ini))

    def _initialize_data_dir_if_needed(self) -> None:
        mysql_system_db = os.path.join(self.data_dir, "mysql")
        if os.path.isdir(mysql_system_db):
            return

        args = [
            self.mysqld_path,
            "--initialize-insecure",
            f"--basedir={self.mysql_root}",
            f"--datadir={self.data_dir}",
            "--console",
        ]
        subprocess.run(args, check=True, creationflags=self._creation_flags())

    def _database_exists(self) -> bool:
        args = self._mysql_base_args() + [
            "-N",
            "-s",
            "-e",
            (
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                f"WHERE SCHEMA_NAME='{self.database}';"
            ),
        ]
        result = self._run_mysql(args, capture_output=True, text=True)
        return bool(result.stdout.strip())

    def _mysql_base_args(self) -> list[str]:
        args = [
            self.mysql_path,
            "-h",
            self.host,
            "-P",
            str(self.port),
            "-u",
            self.user,
            "--protocol=tcp",
            "--default-character-set=utf8mb4",
        ]
        if self.password:
            args.append(f"-p{self.password}")
        return args

    def _wait_for_mysql_ready(self, timeout: int = 15) -> None:
        start = time.time()
        last_error: Optional[Exception] = None
        while time.time() - start < timeout:
            try:
                if os.path.isfile(self.mysqladmin_path):
                    args = [
                        self.mysqladmin_path,
                        "-h",
                        self.host,
                        "-P",
                        str(self.port),
                        "-u",
                        self.user,
                        "ping",
                    ]
                    if self.password:
                        args.append(f"-p{self.password}")
                    self._run_mysql(args, capture_output=True, text=True)
                else:
                    args = self._mysql_base_args() + ["-e", "SELECT 1;"]
                    self._run_mysql(args, capture_output=True, text=True)
                return
            except subprocess.SubprocessError as exc:
                last_error = exc
                time.sleep(0.5)
        if last_error:
            logger.error("MySQL did not become ready: %s", last_error)
        raise TimeoutError(f"MySQL did not become ready within {timeout} seconds.")

    def _run_mysql(
        self,
        args: list[str],
        stdin: Optional[object] = None,
        capture_output: bool = False,
        text: bool = False,
    ) -> subprocess.CompletedProcess:
        try:
            stdout = subprocess.PIPE if capture_output else None
            stderr = subprocess.PIPE
            return subprocess.run(
                args,
                stdin=stdin,
                check=True,
                stdout=stdout,
                stderr=stderr,
                text=text,
                creationflags=self._creation_flags(),
            )
        except subprocess.CalledProcessError as exc:
            stderr = getattr(exc, "stderr", None)
            if isinstance(stderr, bytes):
                stderr = stderr.decode(errors="replace")
            stderr = stderr.strip() if stderr else str(exc)
            logger.error("MySQL command failed: %s", stderr)
            raise

    @staticmethod
    def _is_port_open(host: str, port: int) -> bool:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            return False

    @staticmethod
    def _wait_for_port(host: str, port: int, timeout: int = 10) -> None:
        start = time.time()
        while time.time() - start < timeout:
            if PortableMySQL._is_port_open(host, port):
                return
            time.sleep(0.5)
        raise TimeoutError(f"MySQL did not open port {port} within {timeout} seconds.")

    @staticmethod
    def _creation_flags() -> int:
        if os.name != "nt":
            return 0
        return subprocess.CREATE_NO_WINDOW

    @staticmethod
    def _norm_path(path: str) -> str:
        return os.path.normpath(path).replace("\\", "/")
