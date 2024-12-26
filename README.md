# AlbumWallpaper

## 功能

AlbumWallpaper是一款基于python开发的，跨平台的专辑墙壁纸生成器。


- 输入歌单链接，自动批量下载歌单中每一首歌曲的封面（目前仅支持网易云音乐）。
- 根据文件夹中的所有图片生成一个专辑墙封面。
- 可以自己设定图片，不限定于歌曲封面，只需将图片存放在指定文件夹下即可。
- 可以自己调整生成壁纸的分辨率、长宽比。

## 壁纸展示

![album_wall](https://github.com/user-attachments/assets/80c570df-cf1c-480e-9def-b2fc4ab3b581)



![album_wall](https://github.com/user-attachments/assets/10544e72-371f-4356-bdbf-995374fb88d8)


## 应用展示

<img width="600" alt="image" src="https://github.com/user-attachments/assets/5f61cddf-9deb-4797-810d-8f596ab6afbd" />

## 使用方法

### UI界面
直接在[Release](https://github.com/YanTianlong-01/AlbumWallpaper/releases)中下载对应平台的App即可

### Python运行
- 环境：python3.10
- 拉取：`git clone https://github.com/YanTianlong-01/AlbumWallpaper.git`
- 创建虚拟环境：`python -m venv venv`
- 激活虚拟环境：Windows `.\venv\Scripts\activate`   macOS `source ./venv/bin/activate`
- 安装依赖：`pip install -r requirement.txt`
- 运行App：`python UIMain.py`
- 退出虚拟环境：`deactivate`
