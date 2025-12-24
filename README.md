# Auto Garage Management

PyQt6 desktop app for running an auto garage: vehicle intake, repairs, inventory, billing, and reports.

## Features
- Role-based access (ADMIN, STAFF)
- Vehicle reception, repair orders, lookups
- Payment receipts and revenue reports
- Inventory (stock) reports with stored procedures
- Category/config management and user management

## Tech Stack
- Python 3.10+
- PyQt6 UI
- MySQL 8.0 (portable bundled or system)
- mysql-connector-python, python-dotenv
- Packaging: PyInstaller + Inno Setup (Windows)

## Prerequisites (dev)
- Python 3.10+
- MySQL 8.0 reachable on your host (if not using the bundled portable server)

## Setup for Development
1) Create venv and install deps:
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -e .
```
2) Database: create schema and sample data on MySQL:
```bash
# create DB, tables, triggers, procedures
mysql -u root -p < database/init.sql
# optional sample data
mysql -u root -p < database/data.sql
```
3) Configure env (copy and edit):
```bash
cp .env.example .env
```
Update `.env` with your DB host/port/user/password/name (defaults: host localhost, port 3306, user root, db GarageManagement).

4) Run the app (dev):
```bash
python src/main.py
```

## Windows Packaging (with portable MySQL)
1) Prepare MySQL portable: download MySQL 8.0 x64 ZIP and extract **contents** into `packaging/mysql/` so that `packaging/mysql/bin/mysqld.exe` exists (not nested).
2) Build executable:
```bash
python -m PyInstaller packaging/auto_garage.spec
```
Output: `dist/AutoGarage/AutoGarage.exe` plus `_internal/` data.
3) Build installer:
```bash
iscc packaging/installer.iss
```
Output: `packaging/installer_output/AutoGarageSetup.exe`.
4) Runtime notes (portable MySQL):
- Runs on `127.0.0.1:3307`, user `root`, no password.
- Data stored at `%LOCALAPPDATA%\AutoGarageManagement\mysql`.
- To reset/force re-init (e.g., after schema changes), delete that folder and rerun the app.
- If portable MySQL is missing, the app falls back to system MySQL and uses `.env` / env vars.

## Test Accounts
| Username | Password | Role  |
|----------|----------|-------|
| admin    | admin    | ADMIN |
| staff    | staff    | STAFF |

## Project Structure
```
auto-garage-management/
├───.venv
├───build
├───database
├───dist
│   └───AutoGarage
├───packaging
│   ├───installer_output
│   └───mysql
└───src
    ├───app
    ├───presentation
    │   ├───controllers
    │   ├───views
    │   │   └───pages
    ├───services
    └───utils
```

## License
MIT
