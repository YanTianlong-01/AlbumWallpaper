import os
import re
from netease_music import netease_music
from qq_music import qq_music

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def downloadCover(playlist_url, progress_bar, root, folder_path=BASE_DIR, max_songs=False):
    print('download 1')
    pattern = re.compile(r'(https?://)([^/]+)')
    match = pattern.search(playlist_url)
    if match:
        if match.group(2) == 'music.163.com':
            pattern = re.compile(r'id=([0-9]+)')
            match_id = pattern.search(playlist_url)
            save_path = netease_music(match_id.group(1), folder_path , progress_bar, root, max_songs)
            
        elif match.group(2) == 'y.qq.com':
            pattern = re.compile(r'id=([0-9]+)')
            match_id = pattern.search(playlist_url)
            save_path = qq_music(match_id.group(1), folder_path, progress_bar, root, max_songs)
            
        else:
            print('请输入正确的网易云或者QQ音乐歌单链接')
            return False
    else:
        print('请输入正确的网易云或者QQ音乐歌单链接')
        return False
    print('封面保存到：', save_path)
    return save_path







