# -*- mode: python -*-
block_cipher = None


a = Analysis(['D:\\program\\python\\YouTubeDownLoader\\Main.py'],
             pathex=['D:\\program\\python\\YouTubeDownLoader'],
             binaries=[],
             datas=[
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\key_black.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\key_white.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\link_black.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\link_white.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\logo.ico', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\number_black.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\number_white.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\play_black.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\play_white.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\server_black.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\server_white.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\tool_black.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\icons\\tool_white.svg', 'res\\icons'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\lang\\zh_CN.qm', 'res\\lang'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\lang\\zh_CN.ts', 'res\\lang'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\qss\\light\\sample_interface.qss', 'res\\qss\\light'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\qss\\light\\card_interface.qss', 'res\\qss\\light'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\qss\\light\\scroll_interface.qss', 'res\\qss\\light'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\qss\\light\\video_card.qss', 'res\\qss\\light'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\qss\\dark\\sample_interface.qss', 'res\\qss\\dark'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\qss\\dark\\card_interface.qss', 'res\\qss\\dark'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\qss\\dark\\scroll_interface.qss', 'res\\qss\\dark'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\qss\\dark\\video_card.qss', 'res\\qss\\dark'),
              ('D:\\program\\python\\YouTubeDownLoader\\res\\LICENCE.html', 'res'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher
             )
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='YouTubeDownLoader_V.exe',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir='temp',
          console=True,
          icon='D:\\program\\python\\YouTubeDownLoader\\res\icons\\logo.ico')