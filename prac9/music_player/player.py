import pygame
import os

def load_track(index):
    global total_track_length, current_pos
    if tracks:
        pygame.mixer.music.load(tracks[index])
        current_pos = 0 
        try:
            temp_sound = pygame.mixer.Sound(tracks[index])
            total_track_length = temp_sound.get_length()
        except:
            total_track_length = 180
            
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=8192)
pygame.init()

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = True
pygame.display.set_caption("🎵 Music player")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("consolas", 48, bold=True)
font_med = pygame.font.SysFont("consolas", 32)
font_small = pygame.font.SysFont("consolas", 24)
font_tiny = pygame.font.SysFont("consolas", 18)

BG = (20, 0, 30)
ACCENT = (123, 104, 238)
TEXT = (255, 255, 255)
HIGHLIGHT = (0, 139, 139)

folder = "musics_library"

if not os.path.exists(folder):
    os.makedirs(folder)
    print("musics_library folder was created")
    print("Add some tracks there")

tracks = []
if os.path.exists(folder):
    for file in os.listdir(folder):
        if file.lower().endswith((".mp3", ".wav")):
            tracks.append(os.path.join(folder, file))

if not tracks:
    print(f"No music files in ./{folder}/")
    print("add some MP3 or WAV files and run again")
    
track_names = [os.path.basename(t) for t in tracks]
current_index = 0
current_pos = 0
is_playing = False
volume = 0.5
pygame.mixer.music.set_volume(volume)

total_track_length = 0

def load_track(index):
    """Helper function to load a track and pre-calculate its length."""
    global total_track_length
    if tracks:
        pygame.mixer.music.load(tracks[index])
        
        try:
            temp_sound = pygame.mixer.Sound(tracks[index])
            total_track_length = temp_sound.get_length()
        except:
            total_track_length = 180  

print("\n🎹 Controls:")
print("   P = Play          S = Stop")
print("   N = Next          B = Previous")
print("   Space = Pause/Resume")
print("   ↑/↓ = Volume      ←/→ = Seek ±10s")
print("   Q = Quit\n")

while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if event.type == pygame.KEYDOWN:
            key = event.key
            
            if key == pygame.K_p:
                if not pygame.mixer.get_busy():
                    load_track(current_index)
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.unpause()
                is_playing = True
            
            elif key == pygame.K_s:
                pygame.mixer.music.stop()
                is_playing = False
            
            elif key == pygame.K_d:
                if tracks:
                    pygame.mixer.music.stop()
                    current_index = (current_index + 1) % len(tracks)
                    load_track(current_index)
                    pygame.mixer.music.play()
                    is_playing = True
            
            elif key == pygame.K_a:
                if tracks:
                    pygame.mixer.music.stop()
                    current_index = (current_index - 1) % len(tracks)
                    load_track(current_index)
                    pygame.mixer.music.play()
                    is_playing = True
            
            elif key == pygame.K_q:
                done = False
            
            elif key == pygame.K_SPACE:  
                if pygame.mixer.get_busy():
                    if is_playing:
                        pygame.mixer.music.pause()
                        is_playing = False
                    else:
                        pygame.mixer.music.unpause()
                        is_playing = True
            
            elif key == pygame.K_UP:
                volume = min(1.0, volume + 0.05)
                pygame.mixer.music.set_volume(volume)
            
            elif key == pygame.K_DOWN:
                volume = max(0.0, volume - 0.05)
                pygame.mixer.music.set_volume(volume)
            
            elif key == pygame.K_RIGHT:
                if tracks:
                    current_pos += 10 
                    if current_pos > total_track_length:
                        current_pos = total_track_length
                    pygame.mixer.music.play(start=current_pos)
                    is_playing = True

            elif key == pygame.K_LEFT:
                if tracks:
                    current_pos = max(0, current_pos - 10)
                    pygame.mixer.music.play(start=current_pos)
                    is_playing = True
                

    if is_playing and tracks and not pygame.mixer.music.get_busy():
        current_index = (current_index + 1) % len(tracks)
        load_track(current_index)
        pygame.mixer.music.play()
        
    screen.fill(BG)


    title = font_big.render("MUSIC player", True, ACCENT)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    if not tracks:
        no_music = font_med.render("NO MUSIC FILES IN ./musics_library/", True, (255, 100, 100))
        screen.blit(no_music, (WIDTH // 2 - no_music.get_width() // 2, HEIGHT // 2))
    else:
        current_name = track_names[current_index]
        track_text = font_med.render(f"NOW PLAYING:", True, TEXT)
        name_text = font_small.render(current_name, True, HIGHLIGHT)
        screen.blit(track_text, (60, 120))
        screen.blit(name_text, (60, 160))


        if is_playing or pygame.mixer.music.get_busy():
            elapsed = current_pos + (pygame.mixer.music.get_pos() / 1000)
            

            progress = min(elapsed / total_track_length, 1.0) if total_track_length > 0 else 0

  
            pygame.draw.rect(screen, (50, 50, 80), (60, 220, 680, 20))
            pygame.draw.rect(screen, ACCENT, (60, 220, 680 * progress, 20))


            elapsed_str = f"{int(elapsed//60)}:{int(elapsed%60):02d}"
            total_str = f"{int(total_track_length//60)}:{int(total_track_length%60):02d}"
            time_text = font_small.render(f"{elapsed_str} / {total_str}", True, TEXT)
            screen.blit(time_text, (60, 255))
        else:
            pygame.draw.rect(screen, (50, 50, 80), (60, 220, 680, 20))


        y_offset = 300
        for i, name in enumerate(track_names):
            color = HIGHLIGHT if i == current_index else TEXT
            prefix = "▶ " if i == current_index else f"{i+1:02d}. "
            txt = font_small.render(prefix + name, True, color)
            screen.blit(txt, (60, y_offset))
            y_offset += 35
            if y_offset > HEIGHT - 140:
                break

  
    help_y = HEIGHT - 110
    controls_ui = [("P", "PLAY"), ("A", "BACK"), ("D", "NEXT"), ("S", "STOP"), ("Q", "QUIT")]
    for i, (k, label) in enumerate(controls_ui):
        x_pos = 60 + i * 150
        pygame.draw.rect(screen, (30, 0, 60), (x_pos, help_y, 120, 65), border_radius=8)
        pygame.draw.rect(screen, ACCENT, (x_pos, help_y, 120, 65), 4, border_radius=8)
        key_surf = font_med.render(k, True, (255, 255, 255))
        screen.blit(key_surf, (x_pos + 45, help_y + 8))
        lbl_surf = font_tiny.render(label, True, ACCENT)
        screen.blit(lbl_surf, (x_pos + 35, help_y + 42))

    vol_text = font_small.render(f"Vol: {int(volume*100)}%", True, TEXT)
    screen.blit(vol_text, (WIDTH - 180, HEIGHT - 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print("\n👋 Music player closed. Thanks for listening!")