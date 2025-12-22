# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

spec_dir = os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else os.getcwd()
project_root = os.path.abspath(os.path.join(spec_dir, ".."))
entry_script = os.path.join(project_root, "src", "launcher.py")

datas = [
    (os.path.join(project_root, "database", "init.sql"), "database"),
]

a = Analysis(
    [entry_script],
    pathex=[project_root, os.path.join(project_root, "src")],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AutoGarage",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="AutoGarage",
)
