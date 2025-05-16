# launch_screen.py
import pygame
import os
import sys
import math
import random
import constants as const
from draw_title_button import draw_title, draw_launch_buttons

def load_assets(assets_dir, width, height):
    """Load all game assets (images, fonts, sounds)"""
    assets = {
        'title_image': None,
        'piece_images': [],
        'title_font': None,
        'button_font': None,
        'small_font': None,
        'hover_sound': None,
        'click_sound': None,
        'ambient_sound': None
    }
    
    try:
        # Load title image
        assets['title_image'] = pygame.image.load(os.path.join(assets_dir, 'title.png'))
        assets['title_image'] = pygame.transform.smoothscale(assets['title_image'], (width, height))
        
        # Load chess piece images
        piece_files = ['white_knight.png', 'white_queen.png', 'black_king.png', 
                      'black_rook.png', 'white_pawn.png', 'white_bishop.png', 
                      'black_queen.png', 'black_bishop.png']
        for file in piece_files:
            try:
                img = pygame.image.load(os.path.join(assets_dir, file))
                img = pygame.transform.smoothscale(img, (width//10, width//10))
                assets['piece_images'].append(img)
            except:
                pass
                
        # Load fonts
        title_font_path = os.path.join(assets_dir, 'Bassy.ttf')
        button_font_path = os.path.join(assets_dir, 'Rosemary.ttf')
        subtitle_font_path = os.path.join(assets_dir, 'handsean.ttf')
        
        assets['title_font'] = pygame.font.Font(title_font_path, 60) if os.path.exists(title_font_path) else \
                              pygame.font.SysFont("Times New Roman", 60, bold=True)
        assets['button_font'] = pygame.font.Font(button_font_path, 25) if os.path.exists(button_font_path) else \
            pygame.font.SysFont("Georgia", 25, bold=True)
        assets['small_font'] = pygame.font.Font(subtitle_font_path, 21) if os.path.exists(subtitle_font_path) else \
            pygame.font.SysFont("Arial", 21)
        
        # Load sounds
        pygame.mixer.init()
        assets['hover_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'hover.mp3'))
        assets['click_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'click.wav'))
        assets['ambient_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'ambient.mp3'))
        assets['ambient_sound'].play(0)  # Loop ambient sound
        
    except Exception as e:
        print(f"Error loading assets: {e}")
        # Fallback fonts if loading failed
        assets['title_font'] = pygame.font.SysFont("Times New Roman", 60, bold=True)
        assets['button_font'] = pygame.font.SysFont("Georgia", 25, bold=True)
        assets['small_font'] = pygame.font.SysFont("Arial", 21)
    
    return assets

def create_chess_pieces(piece_images, width, height, count=6):
    """Create animated chess pieces for background"""
    pieces = []
    for _ in range(count):
        if piece_images:
            img = random.choice(piece_images)
            pieces.append({
                'img': img,
                'x': random.randint(0, width),
                'y': random.randint(-height, 0),
                'speed': random.uniform(0.5, 2.0),
                'rotation': 0,
                'rot_speed': random.uniform(-1, 1)
            })
    return pieces

def create_particles(width, height, count=100):
    """Create particle system for background effects"""
    particles = []
    for _ in range(count):
        particles.append({
            'x': random.randint(0, width),
            'y': random.randint(0, height),
            'size': random.randint(2, 6),
            'color': random.choice([const.GOLD, const.ROYAL_BLUE, (255, 255, 255)]),
            'speed': random.uniform(0.2, 1.0)
        })
    return particles

def draw_chess_background(screen, width, height, animation_counter):
    """Draw an animated chess pattern background"""
    square_size = width // 12
    for row in range(height // square_size + 1):
        for col in range(width // square_size + 1):
            color_offset = int(20 * math.sin(animation_counter + (row + col) * 0.2))
            if (row + col) % 2 == 0:
                color = (min(255, 240 + color_offset), 
                        min(255, 217 + color_offset), 
                        min(255, 181 + color_offset))
            else:
                color = (max(0, 181 - color_offset), 
                        max(0, 136 - color_offset), 
                        max(0, 99 - color_offset))
            
            pygame.draw.rect(screen, color, 
                            (col * square_size, row * square_size, square_size, square_size))
    
    # Apply dark overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

def draw_launch_background(screen, assets, width, height, animation_counter, chess_pieces, particles):
    if assets['title_image']:
        offset_x = math.sin(animation_counter * 0.5) * 20
        offset_y = math.cos(animation_counter * 0.3) * 20
        screen.blit(assets['title_image'], (offset_x, offset_y))
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100)) 
        screen.blit(overlay, (0, 0))
    else:
        draw_chess_background(screen, width, height, animation_counter)
    # Animated chess pieces
    for piece in chess_pieces:
        piece['y'] += piece['speed']
        piece['rotation'] += piece['rot_speed']
        if piece['y'] > height:
            piece['y'] = random.randint(-height//2, 0)
            piece['x'] = random.randint(0, width)
        if piece['img']:
            rotated = pygame.transform.rotate(piece['img'], piece['rotation'])
            rot_rect = rotated.get_rect(center=(piece['x'], piece['y']))
            screen.blit(rotated, rot_rect)
    # Particles
    for particle in particles:
        particle['y'] += particle['speed']
        if particle['y'] > height:
            particle['y'] = 0
            particle['x'] = random.randint(0, width)
        size_variation = math.sin(animation_counter * 2 + particle['x']) * 2
        pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), int(particle['size'] + size_variation))

def draw_launch_divider(screen, width, divider_y):
    pygame.draw.line(screen, const.GOLD, (width//4, divider_y), (width*3//4, divider_y), 2)
    for x_pos in [width//4, width//2, width*3//4]:
        pygame.draw.circle(screen, const.GOLD, (x_pos, divider_y), 8)
        pygame.draw.circle(screen, const.BLACK, (x_pos, divider_y), 4)

def draw_launch_subtitle(screen, width, title_bottom, subtitle_font):
    subtitle = "A Battle of Wits & Strategy"
    subtitle_text = subtitle_font.render(subtitle, True, const.WHITE)
    subtitle_rect = subtitle_text.get_rect(midtop=(width//2, title_bottom + 20))
    screen.blit(subtitle_text, subtitle_rect)
    return subtitle_rect.bottom

def create_launch_screen(screen, width, height):
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    assets = load_assets(assets_dir, width, height)
    animation_counter = 0
    particles = create_particles(width, height)
    chess_pieces = create_chess_pieces(assets['piece_images'], width, height)
    button_states = {
        'play': {'hover': False, 'played_sound': False},
        'quit': {'hover': False, 'played_sound': False}
    }
    clock = pygame.time.Clock()
    running = True
    while running:
        animation_counter += 0.03
        mouse_pos = pygame.mouse.get_pos()
        any_hover = False  # Track if any button is hovered
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(mouse_pos):
                    if assets['click_sound']:
                        assets['click_sound'].play()
                    return "PLAY"
                elif quit_button_rect.collidepoint(mouse_pos):
                    if assets['click_sound']:
                        assets['click_sound'].play()
                    pygame.quit()
                    sys.exit()
                    
        # Draw all UI
        draw_launch_background(screen, assets, width, height, animation_counter, chess_pieces, particles)
        
        title_bottom = draw_title(screen, width, height, assets['title_font'], is_launch=True)
        
        subtitle_bottom = draw_launch_subtitle(screen, width, title_bottom, assets['small_font'])
        
        divider_y = subtitle_bottom + 10
        
        draw_launch_divider(screen, width, divider_y)
        
        play_button_rect, quit_button_rect = draw_launch_buttons(
            screen, assets, width, height, animation_counter, button_states)
        
        any_hover = (play_button_rect.collidepoint(mouse_pos) or (quit_button_rect.collidepoint(mouse_pos)))
        
        if any_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
        pygame.display.flip()
        clock.tick(120)
    return "QUIT"