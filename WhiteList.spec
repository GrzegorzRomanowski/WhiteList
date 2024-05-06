# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [
    ('C:\\Dane\\Python\\Wlasne\\WhiteList\\tax.ico', '.'),
    ('C:\\Dane\\Python\\Wlasne\\WhiteList\\tax.png', '.'),
    ('C:\\Dane\\Python\\Wlasne\\WhiteList\\.env', '.')
]
datas += collect_data_files('selenium')


a = Analysis(
    ['C:\\Dane\\Python\\Wlasne\\WhiteList\\main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WhiteList',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='C:\\Dane\\Python\\Wlasne\\WhiteList\\tax.ico'
)
