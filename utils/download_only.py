import yt_dlp
import os

def download_audio_bilibili(url, output_folder="downloads"):
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'overwrites': False,  #  Ne retélécharge pas si le fichier existe déjà
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    while True:
        bilibili_url = input("Enter Bilibili URL (or just Enter to quit): ")
        if not bilibili_url.strip():
            print(" Done. Exiting.")
            break
        download_audio_bilibili(bilibili_url)
        print(" Download complete!\n")
