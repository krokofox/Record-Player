# Record-Player

![Record Player Banner](spotify/banner.png)

## Overview

This project provides a fun and interactive vinyl record player interface for Spotify. Spin the record, scratch for sound effects, and control playback directly from the GUI.

## Physical Build Manual

For detailed instructions on assembling the physical record player enclosure, wiring diagrams, and parts list, please refer to:

- Concept Bytes: https://concept-bytes.com (Search for “Spotify Record Player”)
- Patreon: [Your Patreon Page](https://patreon.com/yourpage)

## Features

- Real-time display of currently playing track, artist, and album art
- Vinyl record spin animation with realistic speed
- Scratch sound effects via swipe gesture
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

1. Create a Spotify application at https://developer.spotify.com/dashboard.
2. Obtain your **Client ID** and **Client Secret**.
3. In `spot.py`, update the following variables:

    ```python
    username = 'your_spotify_username'
    clientID = 'your_client_id'
    clientSecret = 'your_client_secret'
    redirect_uri = 'http://localhost:8888/callback'
    ```

Alternatively, set the following environment variables:

```bash
export SPOTIPY_CLIENT_ID=your_client_id
export SPOTIPY_CLIENT_SECRET=your_client_secret
export SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
export SPOTIPY_USERNAME=your_spotify_username
```

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

- Click and drag on the vinyl record to spin manually.
- Swipe on the record for a scratch effect.
- Click the on-screen buttons:
  - ◄ (Previous track)
  - ▶/⏸ (Play/Pause)
  - ► (Next track)

## Acknowledgments

Built by Concept Bytes. Learn more at https://concept-bytes.com or support on Patreon.
