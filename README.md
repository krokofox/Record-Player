# Record-Player

## Changes by Me (KroKoFox)

Hi, I'm new to GitHub, so please forgive me if I do anything wrong. After having major issues with the Scratch sound, which was monopolizing the sound card,
I decided to remove this feature. While I was at it, I also changed the design to what i like. (spinning Cover Art) Enjoy... Best regards

## Overview

This project provides a fun and interactive vinyl record player interface for Spotify. Spin the record, scratch for sound effects, and control playback directly from the GUI.

## Physical Build Manual

For detailed instructions on assembling the physical record player enclosure, wiring diagrams, and parts list, please refer to:

- Concept Bytes: https://concept-bytes.com (Search for “Spotify Record Player”)
- Patreon: https://patreon.com/ConceptBytes

## Features

- Real-time display of currently playing track, artist, and album art (spinning)
- Vinyl record spin animation with realistic speed
- Playback controls: play/pause, skip forward, skip back
- Random vinyl artwork selection from the `records/` directory

## Requirements

- Python 3.7+
- pip
- Spotify Premium account
- A registered Spotify application (Client ID and Client Secret)

Python dependencies:

```bash
pip install pygame requests spotipy
```

## Configuration

This application uses environment variables for Spotify authentication and settings.
It automatically loads values from a `.env` file in the project root (if present).
Required variables:

- `SPOTIFY_CLIENT_ID`: Your Spotify application Client ID.
- `SPOTIFY_CLIENT_SECRET`: Your Spotify application Client Secret.
- `SPOTIFY_USERNAME`: Your Spotify username.

Optional variables (with defaults):

- `SPOTIFY_REDIRECT_URI` (default: `http://localhost:8888/callback`)
- `SPOTIFY_SCOPE` (default: `user-read-currently-playing`)

To configure, create a `.env` file in the project root with:

```bash
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_USERNAME=your_spotify_username
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
SPOTIFY_SCOPE=user-read-currently-playing
```

Or export them in your shell:

```bash
export SPOTIFY_CLIENT_ID=your_client_id
export SPOTIFY_CLIENT_SECRET=your_client_secret
export SPOTIFY_USERNAME=your_spotify_username
export SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
export SPOTIFY_SCOPE=user-read-currently-playing
```

On first run, if any required variables are missing, the app will prompt you to enter them,
and save them to `.env` for future use.

## Usage

Run the application from the command line:

- Fullscreen mode (default):

  ```bash
  python main.py
  ```

- Windowed mode:

  ```bash
  python main.py --windowed
  ```

Press **ESC** to exit.

## Controls

- Swipe on the record for a scratch effect. (no more sound!)
- Click the on-screen buttons:
  - ◄ (Previous track)
  - ▶/⏸ (Play/Pause)
  - ► (Next track)

## Raspberry Pi Setup (Raspotify)

To use this project with your Raspberry Pi as a Spotify Connect device, install Raspotify:

1. Update packages and install:

   ```bash
   sudo apt update
   sudo apt install raspotify
   ```

   Or run the official installer:

   ```bash
   curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
   ```

2. (Optional) Edit the configuration at `/etc/raspotify/config` to customize:

   ```bash
   sudo nano /etc/raspotify/config
   ```
   For example, set:
   ```
   DEVICE_NAME="My Spotify Pi"
   BITRATE="160"
   ```

3. Restart the service:

   ```bash
   sudo systemctl restart raspotify
   ```

4. In your Spotify app, select your Raspberry Pi (e.g., "raspotify") as the playback device.

Now your Raspberry Pi will appear as a Spotify Connect device.

## Acknowledgments

Built by Concept Bytes. Learn more at https://concept-bytes.com or support on Patreon at https://patreon.com/ConceptBytes.
