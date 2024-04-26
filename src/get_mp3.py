from yt_dlp import YoutubeDL

def get_mp3(url:str,musics:list[str]):
    # 設定(mp3形式にするなど）
    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "outtmpl": "music/%(title)s.%(ext)s", 
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }
    # ダウンロード
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)  # 動画情報を取得
        title = info.get("title")  # 動画のタイトルを取得
        musics.append(f"music/{title}.mp3")
    return f"{title}",musics