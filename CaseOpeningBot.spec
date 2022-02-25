# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['CaseOpeningBot.py'],
             pathex=['C:\\Users\\Tunes\\PycharmProjects\\Case Opening Bot 3.1'],
             binaries=[],
             datas=[('venv\\Lib\\site-packages\\pyfiglet', './pyfiglet')],
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
          name='CaseOpeningBot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='bot.ico')
