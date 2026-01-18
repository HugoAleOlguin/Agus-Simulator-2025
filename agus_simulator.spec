# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

base_path = os.path.dirname(os.path.abspath(SPEC))

# Asegurar que todos los módulos se incluyan
all_hidden_imports = collect_submodules('src') + [
    'src.config',
    'src.utils',
    'src.entities',
    'src.modes',
    'src.effects',
    'src.ui',
    'json',
    'pygame',
    'random',
    'time',
    'math',
    'os',
    'sys'
]

def collect_all_in_dir(dir_path, dest_path):
    result = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(root, base_path)
            result.append((full_path, rel_path))
    return result

a = Analysis(
    ['main.py'],
    pathex=[base_path],
    binaries=[],
    datas=[
        (os.path.join('src', 'assets'), 'src/assets'),
        (os.path.join('src', 'config'), 'src/config'),
        (os.path.join('src', 'utils'), 'src/utils'),
        (os.path.join('src', 'entities'), 'src/entities'),
        (os.path.join('src', 'modes'), 'src/modes'),
        (os.path.join('src', 'effects'), 'src/effects'),
        (os.path.join('src', 'ui'), 'src/ui'),
        (os.path.join('src', 'assets', 'space'), os.path.join('src', 'assets', 'space')),
    ],
    hiddenimports=all_hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'numpy', 'cv2', 'PIL'],  # Excluir módulos no usados
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,  # Mejorar tiempo de carga
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AgusSimulator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Quitar la consola
    icon=os.path.join('src', 'assets', 'ico.ico'),
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AgusSimulator'
)
