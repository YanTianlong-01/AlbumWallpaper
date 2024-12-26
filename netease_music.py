import json
import re
import requests


import os
os.environ['no_proxy'] = '*'


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
}
COOKIES = {"os": "pc"}




def get_play_list(playlist_id):
    url = f"http://music.163.com/playlist?id={playlist_id}" 
    contents = requests.get(url, headers=HEADERS, cookies=COOKIES).text

    playlist_name = re.search(r"<title>(.+)</title>", contents).group(1)[:-13]

    pattern = r'<li><a href="/song\?id=(\d+)">(.+?)</a></li>'
    song_list = re.findall(pattern, contents)

    return playlist_name, song_list


def get_song_info(song_id):
    url = f"http://music.163.com/song?id={song_id}"
    contents = requests.get(url, headers=HEADERS, cookies=COOKIES).text

    pattern = r'<meta property="og:music:artist" content="(.+?)".?/>'
    artist = re.search(pattern, contents).group(1)
    
    pattern = r'<meta property="og:image" content="(.+?)".?/>'
    cover_path = re.search(pattern, contents).group(1)

    pattern = r'<meta property="og:music:album" content="(.+?)".?/>'
    album_name = re.search(pattern, contents)
    if album_name is not None:
        album_name = album_name.group(1)
    else:
        album_name = "Unknown Album"

    return {
        "artist": artist,
        "cover_path": cover_path,
        "album_name": album_name,
    }


def load_song_info(song_id, cache_path):
    out_file = os.path.join(cache_path, f"{song_id}.json")
    if not os.path.exists(out_file):
        return None
    with open(out_file, "r", encoding="utf-8") as f:
        song_info = json.load(f)
    return song_info


def save_song_info(song_info, cache_path):
    song_id = song_info["song_id"]
    out_file = os.path.join(cache_path, f"{song_id}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(song_info, f, ensure_ascii=False, indent=4)


def get_all_song_info(song_list, cache_path, progress_bar, root, max_songs=False):
    song_infos = []
    print("Getting song infos...")

    total_songs = len(song_list)
    progress_bar['maximum'] = total_songs

    # for song_id, song_name in tqdm(song_list):
    for i, (song_id, song_name) in enumerate(song_list):
        if max_songs:
            break_fetch = False
            try:
                max_songs = int(max_songs)
                if max_songs == i:
                    break_fetch = True
            except:
                return False
            if break_fetch:
                break

        song_info_cache = load_song_info(song_id, cache_path)
        if song_info_cache is not None:
            song_infos.append(song_info_cache)
            continue
        try:
            song_info = get_song_info(song_id)
            song_info["song_id"] = song_id
            song_info["song_name"] = song_name
            save_song_info(song_info, cache_path)
            song_infos.append(song_info)
            progress_bar['value'] = i + 1
            root.update()
        except Exception as e:
            print(f"Error on {song_id}")
    return song_infos


def download_covers(song_infos, folder_path, progress_bar, root):
    print("Downloading covers...")
    album = set()
    covers = []

    total_covers = len(song_infos)
    progress_bar['maximum'] = total_covers

    # for song_info in tqdm(song_infos):
    for i, song_info in enumerate(song_infos):

        cover_path = song_info["cover_path"]
        cover_name = cover_path.split("/")[-1]
        album_name = song_info["album_name"]
        if album_name in album:
            continue

        album.add(album_name)
        covers.append(cover_name)
        
        covers_path = os.path.join(folder_path, 'covers')
        os.makedirs(covers_path, exist_ok=True)

        save_path = os.path.join(covers_path, cover_name)

        if os.path.exists(save_path):
            progress_bar['value'] = i + 1
            root.update()
            continue

        r = requests.get(cover_path)
        if r.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(r.content)
        progress_bar['value'] = i + 1
        root.update()

    with open("covers.json", "w", encoding="utf-8") as f:
        json.dump(covers, f, ensure_ascii=False, indent=4)

    return covers_path


def netease_music(paly_list_id, folder_path, progress_bar, root, max_songs=False):
    cache_path = os.path.join(folder_path,'songs')
    os.makedirs(cache_path, exist_ok=True)

    playlist_name, song_list = get_play_list(paly_list_id)
    # print(song_list)

    song_infos = get_all_song_info(song_list, cache_path, progress_bar, root, max_songs)
    save_path = download_covers(song_infos, folder_path, progress_bar, root)
    return save_path


# if __name__ == "__main__":
#     main()