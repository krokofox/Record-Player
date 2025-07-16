import pygame
import os
import random
import sys
import requests
import time
import math
import threading
from io import BytesIO
from spot import get_current_playing_info, start_music, stop_music, skip_to_next, skip_to_previous
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Rundes Bild aus Surface erstellen
def create_circular_surface(source_surf):
    diameter = min(source_surf.get_width(), source_surf.get_height())
    circular_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

    mask = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255, 255), (diameter // 2, diameter // 2), diameter // 2)

    scaled = pygame.transform.smoothscale(source_surf, (diameter, diameter))
    circular_surface.blit(scaled, (0, 0))
    circular_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return circular_surface

def run(windowed=False):
    pygame.display.init()
    pygame.font.init()
    flags = 0 if windowed else pygame.FULLSCREEN
    screen = pygame.display.set_mode((1080, 1080), flags)
    pygame.display.set_caption("Spotify Record Spinner")
    pygame.mouse.set_visible(False)

    # Ressourcen laden
    record_dir = BASE_DIR / 'records'
    record_files = [p for p in record_dir.iterdir() if p.is_file()]
    record_image = pygame.image.load(str(random.choice(record_files)))
    record_image = pygame.transform.scale(record_image, (1350, 1350))

    icons_dir = BASE_DIR / 'spotify'
    play_btn  = pygame.image.load(str(icons_dir / 'play.png'))
    pause_btn = pygame.image.load(str(icons_dir / 'pause.png'))
    skip_btn  = pygame.image.load(str(icons_dir / 'skip.png'))
    prev_btn  = pygame.image.load(str(icons_dir / 'previous.png'))
	
    TRANSPARENCY = 55  # 0 = komplett transparent, 255 = komplett sichtbar

    play_btn.set_alpha(TRANSPARENCY)
    pause_btn.set_alpha(TRANSPARENCY)
    skip_btn.set_alpha(TRANSPARENCY)
    prev_btn.set_alpha(TRANSPARENCY)


    font = pygame.font.Font(None, 40)

    # Zustand
    center = (540, 540)
    angle = 0
    angle_speed = -2.0
    is_playing = True
    dragging = False
    last_mouse_pos = None
    details = None
    album_img = None

    details_lock = threading.Lock()

    def update_details():
        nonlocal details, album_img
        try:
            new_details = get_current_playing_info()
        except Exception as e:
            print(f"Fehler beim Abrufen: {e}", file=sys.stderr)
            return

        if new_details:
            with details_lock:
                details = new_details
                try:
                    r = requests.get(details["album_cover"])
                    img_raw = pygame.image.load(BytesIO(r.content)).convert_alpha()
                    img_scaled = pygame.transform.smoothscale(img_raw, (400, 400))
                    album_img = create_circular_surface(img_scaled)
                except Exception as e:
                    print(f"Fehler beim Laden des Covers: {e}", file=sys.stderr)

    update_details()

    def details_thread():
        while True:
            time.sleep(5)
            update_details()

    threading.Thread(target=details_thread, daemon=True).start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Button-Positionen berechnen
                button_y = 800
                gap = 60

                prev_rect  = prev_btn.get_rect(center=(300, button_y + prev_btn.get_height() // 2))
                pause_rect = pause_btn.get_rect(center=(540, button_y + pause_btn.get_height() // 2))
                skip_rect  = skip_btn.get_rect(center=(780, button_y + skip_btn.get_height() // 2))

                if prev_rect.collidepoint(mx, my):
                    skip_to_previous()
                    threading.Thread(target=update_details, daemon=True).start()
                elif pause_rect.collidepoint(mx, my):
                    if is_playing:
                        stop_music()
                        is_playing = False
                        angle_speed = 0
                    else:
                        start_music()
                        is_playing = True
                        angle_speed = -2.0
                elif skip_rect.collidepoint(mx, my):
                    skip_to_next()
                    record_image = pygame.image.load(str(random.choice(record_files)))
                    record_image = pygame.transform.scale(record_image, (1350, 1350))
                    threading.Thread(target=update_details, daemon=True).start()
                else:
                    if math.hypot(mx - center[0], my - center[1]) <= 540:
                        dragging = True
                        last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - last_mouse_pos[0]
                angle -= dx * 0.1
                angle %= 360
                last_mouse_pos = event.pos

        # Hintergrund
        screen.fill((0, 0, 0))

        # Platte
        rotated_record = pygame.transform.rotate(record_image, angle)
        screen.blit(rotated_record, rotated_record.get_rect(center=center))

        # Album-Cover
        if album_img:
            rotated_album = pygame.transform.rotate(album_img, angle)
            screen.blit(rotated_album, rotated_album.get_rect(center=center))

        # Rotation
        if is_playing:
            angle = (angle + angle_speed) % 360

        # Buttons zeichnen
        screen.blit(prev_btn,  prev_btn.get_rect(center=(300, 800 + prev_btn.get_height() // 2)))
        screen.blit(pause_btn if is_playing else play_btn,
                    (pause_btn if is_playing else play_btn).get_rect(center=(540, 800 + pause_btn.get_height() // 2)))
        screen.blit(skip_btn,  skip_btn.get_rect(center=(780, 800 + skip_btn.get_height() // 2)))

        # Songinfos
        with details_lock:
            if details:
                song_surf = font.render(details["title"], True, (255, 255, 255))
                artist_surf = font.render(details["artist"], True, (255, 255, 255))
                screen.blit(song_surf,   (540 - song_surf.get_width() // 2, 210))
                screen.blit(artist_surf, (540 - artist_surf.get_width() // 2, 160))
                # Silberner Mittelpunkt (Plattenloch)
                pygame.draw.circle(screen, (192, 192, 192), center, 12)  # silberner Ring
                pygame.draw.circle(screen, (100, 100, 100), center, 3)   # dunkler Punkt für Tiefe

        pygame.display.flip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify Record Player")
    parser.add_argument('--windowed', action='store_true', help='Run in windowed mode')
    args = parser.parse_args()
    run(windowed=args.windowed)
