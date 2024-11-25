import os
import subprocess

def download_playlist_with_ytdlp(playlist_url, save_path):
    try:
        os.makedirs(save_path, exist_ok=True)
        print(f"Downloading playlist to {save_path}...")
        
        # yt-dlp command
        command = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio[ext=mp4]/mp4",
            "--yes-playlist",
            "--output", os.path.join(save_path, "%(playlist_index)s - %(title)s.%(ext)s"),
            playlist_url,
        ]
        
        subprocess.run(command)
        print("Playlist download complete.")
    except Exception as e:
        print(f"Error: {e}")

# Usage
if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ").strip()
    save_path = input("Enter the folder to save videos (default: 'Downloads'): ").strip() or "Downloads"
    download_playlist_with_ytdlp(playlist_url, save_path)
