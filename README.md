# Spotify Playlist Audio Downloader (SPAD)

## Prerequisites

- Python 3.6 or higher
- Spotify Developer account and API credentials

## Installation

1. Clone this repository or download the `main.py` script.

2. Install the required Python libraries:

   ```
   pip install spotipy yt-dlp
   ```

3. Set up a Spotify Developer account and create an app to get your Client ID and Client Secret:
   [Read Instructions Here](https://developer.spotify.com/documentation/web-api/concepts/apps)

## Usage

Run the script from the command line with the following arguments:

```
python main.py --client-id YOUR_SPOTIFY_CLIENT_ID --client-secret YOUR_SPOTIFY_CLIENT_SECRET --playlist-url SPOTIFY_PLAYLIST_URL --output-dir OUTPUT_DIRECTORY
```

Replace the following:
- `YOUR_SPOTIFY_CLIENT_ID`: Your Spotify API Client ID
- `YOUR_SPOTIFY_CLIENT_SECRET`: Your Spotify API Client Secret
- `SPOTIFY_PLAYLIST_URL`: The full URL of the Spotify playlist you want to download
- `OUTPUT_DIRECTORY`: The directory where you want to save the downloaded MP3 files (optional, defaults to "downloaded_audio")

Example:

```
python main.py --client-id abc123 --client-secret xyz789 --playlist-url https://open.spotify.com/playlist/37i9dQZF1EpmQ4QVp3CQgu?si=61a2c98671194d3f --output-dir ~/Music/Downloads
```

## Note

This tool is for personal use only. Respect copyright laws and the terms of service of Spotify and YouTube. Make sure you have the right to download and use the audio content.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.