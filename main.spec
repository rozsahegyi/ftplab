# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['d:\\work\\web\\ftplab'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure - [('config', '', '')])
exe = EXE(pyz,
          a.scripts,
          a.binaries - [('config', '', '')],
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'main.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
