# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('database', 'database'),
    ('output', 'output'),
    ('collector', 'collector'),
    ('manager', 'manager'),
    ('models', 'models'),
    ('reports', 'reports'),
    ('utils', 'utils'),
    ('gui', 'gui')],
    hiddenimports=[
    'gui.case_window',
    'gui.main_window',
    'manager.evidence_manager',
    'collector.registry',
    'collector.mounteddevices',
    'collector.event_logs'],
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
    name='USBForensicsAnalyzer',
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
)
