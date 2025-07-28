import yt_dlp
import whisper
import json
import os

def download_audio_bilibili(url, output_folder="downloads"):
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'skip_download': False,
            'overwrites': False,
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
    return filename, info['title']

def transcribe_audio_whisper(audio_path, model_size="base"):
    print(f" Transcribing with Whisper ({model_size})...")
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, verbose=False)
    return result

def save_transcription_json(transcription, title, output_folder="data/transcriptions"):  #  modifié ici
    os.makedirs(output_folder, exist_ok=True)
    segments = [
        {
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        }
        for segment in transcription["segments"]
    ]
    data = {
        "instructional": title,
        "segments": segments
    }
    output_path = os.path.join(output_folder, f"{title}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f" Transcription saved: {output_path}")

if __name__ == "__main__":
    bilibili_url = input("Enter Bilibili URL (leave empty if already downloaded): ")

    if bilibili_url.strip():
        audio_file, title = download_audio_bilibili(bilibili_url)

    for file in os.listdir("downloads"):
        if file.endswith(".mp3"):
            json_name = file.replace(".mp3", ".json")
            if json_name in os.listdir("data/transcriptions"):  #  modifié ici aussi
                print(f"⏩ Already transcribed: {file}, skipping...")
                continue

            print(f"\n🎧 Transcribing: {file}")
            transcription = transcribe_audio_whisper(f"downloads/{file}", model_size="base")
            save_transcription_json(transcription, file.replace(".mp3", ""))
