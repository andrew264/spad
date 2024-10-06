import argparse
import os
import queue
import threading
import time

import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp

NUM_THREADS = 8
SONG_LIMIT = 100


def get_playlist_tracks(sp: Spotify, playlist_id: str):
    start = time.time()
    results = sp.playlist_items(playlist_id, limit=SONG_LIMIT)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    print(f"Fetched Playlist in {(time.time()-start):.2f} s")
    return tracks


def queue_tracks(tracks, download_queue: queue.Queue):
    for track in tracks:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        search_query = f"{track_name} {artist_name}"
        download_queue.put(search_query)
    print(f"Added {len(tracks)} tracks to download queue")


def download_worker(download_queue: queue.Queue, output_dir: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'default_search': 'ytsearch',
        'quiet': True,
        'no_warnings': True,
    }

    while True:
        search_query = download_queue.get()
        if search_query is None:
            break
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch1:{search_query}", download=False)['entries'][0]
                url = result['webpage_url']
                ydl.download([url])
            print(f"Downloaded: {search_query}")
        except Exception as e:
            print(f"Error processing {search_query}: {str(e)}")
        finally:
            download_queue.task_done()


def main(client_id: str, client_secret: str, playlist_url: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    tracks = get_playlist_tracks(sp, playlist_id)

    download_queue = queue.Queue()
    queue_tracks(tracks, download_queue)

    start = time.time()
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=download_worker, args=(download_queue, output_dir))
        t.start()
        threads.append(t)
    download_queue.join()

    for _ in range(NUM_THREADS):
        download_queue.put(None)
    for t in threads:
        t.join()

    print(f"All downloads completed in {(time.time()-start):.2f} sec")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download audio from Spotify playlist using YouTube")
    parser.add_argument("--client-id", required=True, help="Spotify API client ID")
    parser.add_argument("--client-secret", required=True, help="Spotify API client secret")
    parser.add_argument("--playlist-url", required=True, help="Spotify playlist URL")
    parser.add_argument("--output-dir", default="downloaded_audio", help="Directory to save downloaded audio files")

    args = parser.parse_args()

    main(args.client_id, args.client_secret, args.playlist_url, args.output_dir)
