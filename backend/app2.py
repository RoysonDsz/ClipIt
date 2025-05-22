import yt_dlp

url = "https://www.youtube.com/watch?v=t-WAGCR-Ez8"

ydl_opts = {
    'format': 'best',
    'outtmpl': 'downloaded_video.%(ext)s'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])