# Auto Garage Management System

A PyQt6 desktop application for managing an auto garage business.

## Features

- User authentication with role-based access control
- Vehicle reception management (Tiep nhan xe)
- Repair order management (Phieu sua chua)
- Vehicle lookup (Tra cuu xe)
- Payment receipts (Phieu thu)
- Revenue reports (Bao cao doanh so)
- Inventory reports (Bao cao ton)
- Category management (Quan ly danh muc)
- System configuration (Thay doi quy dinh)
- User management (Quan ly user)

## Roles

- **ADMIN**: Full access to all features
- **STAFF**: Access to vehicle reception, repair orders, vehicle lookup, and payment receipts only

## Requirements

- Python 3.10 or higher
- PyQt6
- MySQL Server 8.0 or higher
- mysql-connector-python
- python-dotenv

## Installation

### 1. Install MySQL Server

Make sure you have MySQL Server installed and running on your machine.

### 2. Create Database

Run the SQL scripts to create the database and tables:

```bash
# Connect to MySQL
mysql -u root -p

# Create database and tables
mysql -u root -p < database/TABLE+trigger.sql

# Insert sample data (optional)
mysql -u root -p < database/data.sql
```

### 3. Configure Database Connection

Copy the `.env.example` file to `.env` and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=GarageManagement
```

### 4. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install mysql-connector-python python-dotenv PyQt6
```

Or install from pyproject.toml:

```bash
pip install -e .
```

## Running the Application

```bash
cd src
python main.py
```

## Test Credentials

| Username | Password | Role  |
|----------|----------|-------|
| admin    | admin    | ADMIN |
| staff    | staff    | STAFF |

## Project Structure

```
auto-garage-management/
    pyproject.toml
    README.md
    src/
        main.py
        app/
            __init__.py
            session.py
        presentation/
            __init__.py
            permissions.py
            views/
                __init__.py
                login_dialog.py
                main_window.py
                pages/
                    __init__.py
                    tiep_nhan_xe_page.py
                    phieu_sua_chua_page.py
                    tra_cuu_xe_page.py
                    phieu_thu_page.py
                    bao_cao_doanh_so_page.py
                    bao_cao_ton_page.py
                    quan_ly_danh_muc_page.py
                    thay_doi_quy_dinh_page.py
                    quan_ly_user_page.py
            controllers/
                __init__.py
                login_controller.py
                main_controller.py
        utils/
            __init__.py
            messages.py
```

## License

MIT License
