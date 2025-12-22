# Packaging (Windows)

This folder sets up a Windows installer that bundles a portable MySQL runtime.

## 1) Prepare MySQL portable

Download the MySQL 8.0 ZIP archive for Windows (x64) and extract it to:

```
packaging/mysql/
  bin/
  lib/
  share/
  ...
```

Make sure `packaging/mysql/bin/mysqld.exe` exists.

## 2) Build the app with PyInstaller

From the repository root:

```bash
python -m PyInstaller packaging/auto_garage.spec
```

Output goes to `dist/AutoGarage/AutoGarage.exe`.

If you want to test locally without the installer, copy the MySQL folder:

```bash
xcopy /E /I packaging\mysql dist\AutoGarage\mysql
```

## 3) Build the installer (Inno Setup)

Install Inno Setup and run:

```bash
iscc packaging/installer.iss
```

The installer output is written to `packaging/installer_output/`.

## Notes

- MySQL data files are stored in `%LOCALAPPDATA%\AutoGarageManagement\mysql\data`.
- Logs are written to `%LOCALAPPDATA%\AutoGarageManagement\logs\launcher.log`.
