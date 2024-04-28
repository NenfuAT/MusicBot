from yt_dlp import YoutubeDL
import asyncio
async def get_mp3(url: str, musics: list[str]):
    title=""
    # 設定(mp3形式にするなど）
    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "outtmpl": "music/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            },
        ],
    }
    
    # ダウンロード処理を非同期タスクとして実行
    def sync_download():
        global title
        # YouTubeから情報を取得
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)  # 動画情報を取得（ダウンロードは行わない）
            title = info.get("title")  # 動画のタイトルを取得
            music_path = f"music/{title}.mp3"
            
            # 曲がリストにすでに存在するかチェック
            if music_path in musics:
                return f"{title} はすでにリストにあります", musics
            
            # ダウンロード
            ydl.download([url])  # 指定された URL をダウンロード
            musics.append(music_path)  # 新しい曲をリストに追加
    # 非同期でダウンロード
    await asyncio.to_thread(sync_download)  # スレッドで非同期処理
    return f"{url}\n{title}を追加しました", musics
