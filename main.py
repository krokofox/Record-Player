import pygame
import os
import random
import sys
import requests
import time
import math
from io import BytesIO
from spot import get_current_playing_info, start_music, stop_music, skip_to_next, skip_to_previous
import argparse

def run(windowed=False):
    # Initialize Pygame and audio mixer
    pygame.init()
    pygame.mixer.init()
    flags = 0 if windowed else pygame.FULLSCREEN
    screen = pygame.display.set_mode((1080, 1080), flags)
    pygame.display.set_caption("Spotify Record Spinner")

    # -------------------------------
    # Load & scale images
    # -------------------------------
    record_dir = './records'
    record_files = [
        os.path.join(record_dir, f)
        for f in os.listdir(record_dir)
        if os.path.isfile(os.path.join(record_dir, f))
    ]
    random_record_path = random.choice(record_files)
    record_image = pygame.image.load(random_record_path)
    record_image = pygame.transform.scale(record_image, (int(1080 * 1.25), int(1080 * 1.25)))

    play_btn  = pygame.image.load('./spotify/play.png')
    pause_btn = pygame.image.load('./spotify/pause.png')
    skip_btn  = pygame.image.load('./spotify/skip.png')
    prev_btn  = pygame.image.load('./spotify/previous.png')
    banner    = pygame.image.load('./spotify/banner.png')

    font = pygame.font.Font(None, 40)

    # -------------------------------
    # Load scratch sound effects
    # -------------------------------
    sfx_dir = './sfx'
    sfx_paths = [
        os.path.join(sfx_dir, fn)
        for fn in os.listdir(sfx_dir)
        if fn.lower().endswith('.wav')
    ]
    scratch_sounds = [pygame.mixer.Sound(path) for path in sfx_paths]

    # -------------------------------
    # State variables
    # -------------------------------
    center = (540, 540)
    angle = 0
    angle_speed = -0.5
    is_playing = True
    dragging = False
    last_mouse_pos = None
    last_check = 0
    details = None
    album_img = None

    # Swipe detection
    swipe_start_pos = None
    swipe_start_time = None
    SWIPE_DIST  = 100    # Minimum pixels moved
    SWIPE_TIME  = 0.5    

    while True:
        # Fetch Spotify info every 5 seconds
        if time.time() - last_check > 5:
            details = get_current_playing_info()
            last_check = time.time()
            if details:
                r = requests.get(details["album_cover"])
                album_img = pygame.image.load(BytesIO(r.content))
                album_img = pygame.transform.scale(album_img, (137, 137))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Exit on ESC
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            # Mouse down: record swipe start & handle clicks
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                swipe_start_pos = event.pos
                swipe_start_time = time.time()
                mx, my = event.pos

                # Compute control positions
                banner_x = (1080 - banner.get_width()) // 2
                banner_y = 800
                gap = 51
                album_w, album_h = (137, 137) if album_img else (0, 0)
                prev_w, prev_h   = prev_btn.get_width(), prev_btn.get_height()
                pause_w, pause_h = pause_btn.get_width(), pause_btn.get_height()
                skip_w, skip_h   = skip_btn.get_width(), skip_btn.get_height()

                group_width   = album_w + prev_w + pause_w + skip_w + (3 * gap)
                group_start_x = (1080 - group_width) // 2
                group_center_y = banner_y + (banner.get_height() // 2) + 30

                album_x = group_start_x
                album_y = (group_center_y - (album_h // 2)) - 30
                prev_x  = album_x + album_w + gap
                prev_y  = group_center_y - (prev_h // 2)
                pause_x = prev_x + prev_w + gap
                pause_y = group_center_y - (pause_h // 2)
                skip_x  = pause_x + pause_w + gap
                skip_y  = group_center_y - (skip_h // 2)

                # Previous track
                if prev_x <= mx <= prev_x + prev_w and prev_y <= my <= prev_y + prev_h:
                    skip_to_previous()
                    details = get_current_playing_info(); last_check = time.time()
                    if details:
                        r = requests.get(details["album_cover"])
                        album_img = pygame.image.load(BytesIO(r.content))
                        album_img = pygame.transform.scale(album_img, (137, 137))

                # Play/pause toggle
                elif pause_x <= mx <= pause_x + pause_w and pause_y <= my <= pause_y + pause_h:
                    if is_playing:
                        stop_music()
                        is_playing = False
                        angle_speed = 0
                    else:
                        start_music()
                        is_playing = True
                        angle_speed = -0.5

                # Next track & load new record art
                elif skip_x <= mx <= skip_x + skip_w and skip_y <= my <= skip_y + skip_h:
                    skip_to_next()
                    new_path = random.choice(record_files)
                    record_image = pygame.image.load(new_path)
                    record_image = pygame.transform.scale(record_image, (int(1080 * 1.25), int(1080 * 1.25)))
                    details = get_current_playing_info(); last_check = time.time()
                    if details:
                        r = requests.get(details["album_cover"])
                        album_img = pygame.image.load(BytesIO(r.content))
                        album_img = pygame.transform.scale(album_img, (137, 137))

                # Otherwise, start dragging if click on record
                else:
                    if math.hypot(mx - center[0], my - center[1]) <= 540:
                        dragging = True
                        last_mouse_pos = event.pos

            # Mouse up: check for swipe & stop dragging
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if swipe_start_pos and swipe_start_time:
                    dx = event.pos[0] - swipe_start_pos[0]
                    dy = event.pos[1] - swipe_start_pos[1]
                    dist = math.hypot(dx, dy)
                    elapsed = time.time() - swipe_start_time
                    if dist > SWIPE_DIST and elapsed < SWIPE_TIME:
                        random.choice(scratch_sounds).play()

                dragging = False
                swipe_start_pos = None
                swipe_start_time = None

            # Dragging motion rotates the record
            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - last_mouse_pos[0]
                angle -= dx * 0.1
                angle %= 360
                last_mouse_pos = event.pos

        # -------------------------------
        # Drawing
        # -------------------------------
        screen.fill((245, 230, 200))

        # Spinning record
        rotated = pygame.transform.rotate(record_image, angle)
        screen.blit(rotated, rotated.get_rect(center=center))
        if is_playing:
            angle = (angle + angle_speed) % 360

        # Banner
        banner_x = (1080 - banner.get_width()) // 2
        banner_y = 800
        screen.blit(banner, (banner_x, banner_y))

        # Control group layout
        gap = 51
        album_w, album_h = (137, 137) if album_img else (0, 0)
        prev_w, prev_h   = prev_btn.get_width(), prev_btn.get_height()
        pause_w, pause_h = pause_btn.get_width(), pause_btn.get_height()
        skip_w, skip_h   = skip_btn.get_width(), skip_btn.get_height()

        group_width   = album_w + prev_w + pause_w + skip_w + (3 * gap)
        group_start_x = (1080 - group_width) // 2
        group_center_y = banner_y + (banner.get_height() // 2) + 30

        album_x = group_start_x
        album_y = (group_center_y - (album_h // 2)) - 30
        prev_x  = album_x + album_w + gap
        prev_y  = group_center_y - (prev_h // 2)
        pause_x = prev_x + prev_w + gap
        pause_y = group_center_y - (pause_h // 2)
        skip_x  = pause_x + pause_w + gap
        skip_y  = group_center_y - (skip_h // 2)

        if album_img:
            screen.blit(album_img, (album_x, album_y))
        screen.blit(prev_btn,  (prev_x,  prev_y))
        screen.blit(pause_btn if is_playing else play_btn, (pause_x, pause_y))
        screen.blit(skip_btn,  (skip_x,  skip_y))

        # Song text
        if details:
            song_surf   = font.render(details["title"],  True, (255, 255, 255))
            artist_surf = font.render(details["artist"], True, (255, 255, 255))
            pcx = pause_x + pause_w // 2
            tb  = pause_y - 10
            ay  = tb - artist_surf.get_height()
            sy  = ay - 5 - song_surf.get_height()
            sx  = pcx - (song_surf.get_width()   // 2)
            ax  = pcx - (artist_surf.get_width() // 2)
            screen.blit(song_surf,   (sx, sy))
            screen.blit(artist_surf, (ax, ay))

        pygame.display.flip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify Record Player")
    parser.add_argument('--windowed', action='store_true', help='Run in windowed mode (no fullscreen)')
    args = parser.parse_args()
    run(windowed=args.windowed)
