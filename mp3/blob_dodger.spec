# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['blob_dodger.py'],
             pathex=['O:\\OneDrive\\repos\\Python\\Games\\blob_dodger_rects\\mp3'],
             binaries=[],
             datas=[('/mp3/bg_music', '/mp3/bg_music')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='blob_dodger',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
