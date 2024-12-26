import tkinter as tk
from tkinter import filedialog
from downloadPlaylistCovers import downloadCover
from createWallpaper import createWallpaper
import os
from tkinter.ttk import Progressbar
from tkinter import messagebox
import json
from PIL import Image, ImageTk
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("专辑墙纸制作器")
        self.geometry("600x550")  # 设置窗口大小
        self.download_path = BASE_DIR  # 默认路径
        self.save_path = None
        self.wallpaper_path = None
        self.max_songs = None
        self.load_settings()
        self.init_ui()
        self.lift()

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
                self.download_path = settings.get("download_path", BASE_DIR)
                self.save_path = self.download_path
        except FileNotFoundError:
            pass  # Use default values if the file doesn't exist
        except json.JSONDecodeError:
            pass # Use default values if the file is corrupted

    def save_settings(self):
        settings = {"download_path": self.download_path}
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)

    def init_ui(self):
        # 标题部分
        title_label = tk.Label(
            self, text="专辑墙纸制作器", font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=10)

        title_label = tk.Label(
            self, text="具体操作：\n第一步 输入歌单链接（目前仅支持网易云音乐）\n第二步 批量下载封面 \n第三步 制作壁纸", font=('Helvetica', 12), justify="left"
        )
        title_label.pack(pady=10)

        # 歌单链接部分
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        playlist_label = tk.Label(input_frame, text="输入歌单链接:", font=(12))
        playlist_label.grid(row=0, column=0, padx=5, pady=5)

        self.playlist_entry = tk.Entry(input_frame, width=50, font=(12))
        self.playlist_entry.grid(row=0, column=1, padx=5, pady=5)

        # 最大下载歌曲数量
        max_songs_fram = tk.Frame(self)
        max_songs_fram.pack(pady=10)
        max_songs_label = tk.Label(max_songs_fram, text="最大下载歌曲数量")
        max_songs_label.grid(row=0, column=0,padx=5, pady=5)
        self.max_songs_entry = tk.Entry(max_songs_fram, width=6, font=(12))
        self.max_songs_entry.grid(row=0, column=1,padx=5, pady=5)

        # 下载路径部分
        path_frame = tk.Frame(self)
        path_frame.pack(pady=10)

        select_folder_button = tk.Button(
            path_frame, text="选择下载路径", command=self.select_folder, font=(12)
        )
        select_folder_button.grid(row=0, column=0, padx=5, pady=5)

        self.download_path_label = tk.Label(
            path_frame, text=" ", font=(12)
        )
        self.download_path_label.grid(row=0, column=1, padx=5, pady=5)
        self.update_download_path_label()

        # 进度条部分
        self.progress_bar = Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=20)

        # 操作按钮部分
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        download_cover_button = tk.Button(
            button_frame, text="批量下载封面", command=self.start_download, font=(12)
        )
        download_cover_button.grid(row=0, column=0, padx=10)

        create_wallpaper_button = tk.Button(
            button_frame, text="制作壁纸", command=self.start_create_wallpaper, font=(12)
        )
        create_wallpaper_button.grid(row=0, column=1, padx=10)

        # 壁纸大小设置
        size_frame = tk.Frame(self)
        size_frame.pack(pady=10)

        width_label = tk.Label(size_frame, text="壁纸宽度:", font=(12))
        width_label.grid(row=0, column=0, padx=5, pady=5)

        self.width_entry = tk.Entry(size_frame, width=10, font=(12))
        self.width_entry.grid(row=0, column=1, padx=5, pady=5)
        self.width_entry.insert(0, "1920")  # 默认宽度

        height_label = tk.Label(size_frame, text="壁纸高度:", font=(12))
        height_label.grid(row=0, column=2, padx=5, pady=5)

        self.height_entry = tk.Entry(size_frame, width=10, font=(12))
        self.height_entry.grid(row=0, column=3, padx=5, pady=5)
        self.height_entry.insert(0, "1080")  # 默认高度

        # 状态面板
        self.status_label = tk.Text(
            self, font=(12), height=3, wrap="word"
        )
        self.status_label.pack(pady=20)
        self.status_label.config(state=tk.DISABLED)

        # GitHub 链接按钮
        github_button = tk.Button(self, text="查看项目Github", command=self.open_github, font=(12))
        github_button.pack(pady=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory(initialdir=self.download_path)
        if folder_path:
            self.download_path = folder_path
            self.update_download_path_label()
            self.save_path = folder_path
            self.save_settings()

    def update_download_path_label(self):
        parts = self.download_path.split('/')
        if len(parts) > 4:
            truncated_path = "/".join(parts[:3]) + "/.../" + "/".join(parts[-2:])
            self.download_path_label.config(text=" " + truncated_path)
        else:
            self.download_path_label.config(text=" " + self.download_path)

    def start_download(self):
        playlist_url = self.playlist_entry.get()
        if playlist_url:
            self.info_status_label("下载中...")
            self.max_songs = self.max_songs_entry.get()
            # 假设 downloadCover 是实现的下载函数
            self.save_path = downloadCover(playlist_url, self.progress_bar, self, self.download_path, self.max_songs)
            if not self.save_path:
                messagebox.showerror('请输入正确的网易云歌单链接!')
            else:
                self.info_status_label(f"封面已下载完成，保存在文件夹: {self.save_path}")
        else:
            messagebox.showerror("错误", "请输入歌单链接")
        self.progress_bar['value'] = 0
        self.update()

    def start_create_wallpaper(self):
        if self.save_path:
            self.info_status_label("创建壁纸中...")

            width = self.width_entry.get()
            height = self.height_entry.get()
            try :
                width = int(width)
                height = int(height)
            except:
                messagebox.showerror("错误", "请在壁纸高宽设置中输入纯数字！")
                self.clear_status_label()
                return
            self.wallpaper_path = createWallpaper(self.save_path)
            if not self.wallpaper_path:
                messagebox.showerror("错误", "请在确保路径中存在图片！")
                self.clear_status_label()
                return
            else:
                self.info_status_label(f"壁纸已经创建完成，保存在文件夹: {self.wallpaper_path}")
                self.show_wallpaper()

        else:
            messagebox.showerror("错误", "请先下载封面")
            return
    
    def clear_status_label(self):
        self.status_label.config(state=tk.NORMAL)
        self.status_label.delete("1.0", tk.END)
        self.status_label.config(state=tk.DISABLED)
        self.update()

    def info_status_label(self, info_text):
        self.status_label.config(state=tk.NORMAL)
        self.status_label.delete("1.0", tk.END)
        self.status_label.insert(tk.END, info_text)
        self.status_label.config(state=tk.DISABLED)
        self.update()

    def show_wallpaper(self): 
        if self.wallpaper_path: 
            try: 
                wallpaper_window = tk.Toplevel(self) 
                wallpaper_window.title("生成的壁纸") 
                image = Image.open(self.wallpaper_path) 
                photo = ImageTk.PhotoImage(image) 
                label = tk.Label(wallpaper_window, image=photo) 
                label.image = photo 
                label.pack() 
            except Exception as e: 
                messagebox.showerror("错误", f"无法显示壁纸: {e}")

    def open_github(self):
        webbrowser.open("https://github.com/YanTianlong-01/AlbumWallpaper")
    


if __name__ == '__main__':
    app = App()
    app.mainloop()
