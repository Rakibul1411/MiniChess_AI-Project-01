# launch_screen.py
import pygame
import os
import sys
import math
import random
import constants as const

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
        title_font_path = os.path.join(assets_dir, 'medieval.ttf')
        button_font_path = os.path.join(assets_dir, 'fantasy.ttf')
        
        assets['title_font'] = pygame.font.Font(title_font_path, 90) if os.path.exists(title_font_path) else \
                              pygame.font.SysFont("Times New Roman", 90, bold=True)
        assets['button_font'] = pygame.font.Font(button_font_path, 48) if os.path.exists(button_font_path) else \
                               pygame.font.SysFont("Georgia", 48, bold=True)
        assets['small_font'] = pygame.font.SysFont("Arial", 24)
        
        # Load sounds
        pygame.mixer.init()
        assets['hover_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'hover.wav'))
        assets['click_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'click.wav'))
        assets['ambient_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'ambient.wav'))
        assets['ambient_sound'].play(-1)  # Loop ambient sound
        
    except Exception as e:
        print(f"Error loading assets: {e}")
        # Fallback fonts if loading failed
        assets['title_font'] = pygame.font.SysFont("Times New Roman", 90, bold=True)
        assets['button_font'] = pygame.font.SysFont("Georgia", 48, bold=True)
        assets['small_font'] = pygame.font.SysFont("Arial", 24)
    
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

def draw_title(screen, width, height, title_font, small_font, animation_counter):
    """Draw the animated title with effects"""
    title_text = "MINI CHESS"
    title_offset = math.sin(animation_counter) * 10
    
    # Create title surface
    title_surface = pygame.Surface((width, 200), pygame.SRCALPHA)
    
    # Shadow effect
    shadow_text = title_font.render(title_text, True, (0, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(width//2 + 5, 100 + 5))
    title_surface.blit(shadow_text, shadow_rect)
    
    # Gradient title text
    for i in range(90):
        gradient_color = (
            max(0, min(255, int(const.GOLD[0] * (1 - i/180) + const.ROYAL_BLUE[0] * (i/180)))),
            max(0, min(255, int(const.GOLD[1] * (1 - i/180) + const.ROYAL_BLUE[1] * (i/180)))),
            max(0, min(255, int(const.GOLD[2] * (1 - i/180) + const.ROYAL_BLUE[2] * (i/180))))
        )
        line_text = title_font.render(title_text, True, gradient_color)
        title_surface.blit(line_text, (shadow_rect.x, shadow_rect.y - 90 + i))
    
    title_rect = title_surface.get_rect(center=(width//2, height//4 + title_offset))
    
    # Glow effect
    pulse = (math.sin(animation_counter * 2) + 1) * 0.5
    for i in range(20, 0, -4):
        glow_surf = pygame.Surface((title_rect.width + i*2, title_rect.height + i*2), pygame.SRCALPHA)
        glow_alpha = int(50 - i*2 + 30 * pulse)
        glow_color = (const.GOLD[0], const.GOLD[1], const.GOLD[2], glow_alpha)
        pygame.draw.rect(glow_surf, glow_color, 
                        (0, 0, title_rect.width + i*2, title_rect.height + i*2), 
                        border_radius=25)
        screen.blit(glow_surf, (title_rect.x - i, title_rect.y - i))
    
    screen.blit(title_surface, title_rect)
    
    # Subtitle
    subtitle = "A Battle of Wits & Strategy"
    chars_to_show = min(len(subtitle), int((animation_counter * 3) % (len(subtitle) + 20)))
    visible_text = subtitle[:chars_to_show] if chars_to_show < len(subtitle) else subtitle
    
    subtitle_text = small_font.render(visible_text, True, const.WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(width//2, height//4 + 90))
    screen.blit(subtitle_text, subtitle_rect)

def draw_divider(screen, width, height):
    """Draw ornate divider between title and buttons"""
    divider_y = height//2 - 30
    pygame.draw.line(screen, const.GOLD, (width//4, divider_y), (width*3//4, divider_y), 2)
    
    # Add ornaments to divider
    ornament_size = 12
    for x_pos in [width//4, width//2, width*3//4]:
        pygame.draw.circle(screen, const.GOLD, (x_pos, divider_y), ornament_size)
        pygame.draw.circle(screen, const.BLACK, (x_pos, divider_y), ornament_size-4)
        pygame.draw.circle(screen, const.GOLD, (x_pos, divider_y), ornament_size-8)

def create_button(screen, rect, text, font, color, hover_color, 
                 piece_img=None, hover_effect=True, animation_counter=0):
    """Create a fancy button with hover effects"""
    mouse_pos = pygame.mouse.get_pos()
    hover = rect.collidepoint(mouse_pos)
    
    # Button scaling and color effects
    if hover and hover_effect:
        glow = (math.sin(animation_counter * 5) + 1) * 0.5
        btn_color = (
            int(color[0] * (0.8 + 0.2 * glow)),
            int(color[1] * (0.8 + 0.2 * glow)),
            int(color[2] * (0.8 + 0.2 * glow))
        )
        scale = 1.05
    else:
        btn_color = color
        scale = 1.0
    
    # Calculate scaled dimensions
    scaled_width = int(rect.width * scale)
    scaled_height = int(rect.height * scale)
    scaled_x = rect.x - (scaled_width - rect.width) // 2
    scaled_y = rect.y - (scaled_height - rect.height) // 2
    scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
    
    # Create gradient fill
    gradient = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
    for i in range(scaled_height):
        intensity = 1.2 - (i / scaled_height) * 0.8
        grad_color = (
            min(255, int(btn_color[0] * intensity)),
            min(255, int(btn_color[1] * intensity)),
            min(255, int(btn_color[2] * intensity))
        )
        pygame.draw.line(gradient, grad_color, (0, i), (scaled_width, i))
    
    # Draw button with rounded corners
    pygame.draw.rect(gradient, (0, 0, 0, 100), 
                    (0, 0, scaled_width, scaled_height), 
                    border_radius=30)
    screen.blit(gradient, (scaled_x, scaled_y))
    
    # Draw glow border if hovered
    if hover and hover_effect:
        for i in range(5, 0, -1):
            border_color = (
                min(255, int(const.WHITE[0] * (0.5 + 0.1 * i))),
                min(255, int(const.WHITE[1] * (0.5 + 0.1 * i))),
                min(255, int(const.WHITE[2] * (0.5 + 0.1 * i)))
            )
            pygame.draw.rect(screen, border_color, 
                            (scaled_x-i, scaled_y-i, 
                            scaled_width+i*2, scaled_height+i*2), 
                            3, border_radius=30+i)
    
    # Main border
    pygame.draw.rect(screen, const.WHITE, 
                    (scaled_x, scaled_y, scaled_width, scaled_height), 
                    3, border_radius=30)
    
    # Add chess piece icon if provided
    if piece_img:
        piece_size = scaled_height-20
        img = pygame.transform.smoothscale(piece_img, (piece_size, piece_size))
        screen.blit(img, (scaled_x + 15, scaled_y + 10))
    
    # Button text with animation
    text_surf = font.render(text, True, const.WHITE)
    text_rect = text_surf.get_rect(center=(scaled_x + scaled_width//2 + 15, 
                                         scaled_y + scaled_height//2))
    
    if hover and hover_effect:
        text_rect.y -= int(4 * math.sin(animation_counter * 8))
    
    screen.blit(text_surf, text_rect)
    
    return hover, scaled_rect

def create_launch_screen(screen, width, height):
    """Main launch screen function"""
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    
    # Load all assets
    assets = load_assets(assets_dir, width, height)
    
    # Animation and game objects
    animation_counter = 0
    particles = create_particles(width, height)
    chess_pieces = create_chess_pieces(assets['piece_images'], width, height)
    
    # Button state tracking
    button_states = {
        'play': {'hover': False, 'played_sound': False},
        'quit': {'hover': False, 'played_sound': False}
    }
    
    # Main loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        animation_counter += 0.03
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    if assets['click_sound']:
                        assets['click_sound'].play()
                    return "PLAY"
                elif quit_button_rect.collidepoint(mouse_pos):
                    if assets['click_sound']:
                        assets['click_sound'].play()
                    pygame.quit()
                    sys.exit()
        
        # Draw background
        if assets['title_image']:
            # Parallax scrolling effect
            offset_x = math.sin(animation_counter * 0.5) * 20
            offset_y = math.cos(animation_counter * 0.3) * 20
            screen.blit(assets['title_image'], (offset_x, offset_y))
            
            # Dark overlay with gradient
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            for y in range(height):
                alpha = 180 - 50 * math.sin(y / height * math.pi)
                pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (width, y))
            screen.blit(overlay, (0, 0))
        else:
            draw_chess_background(screen, width, height, animation_counter)
        
        # Update and draw falling chess pieces
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
        
        # Update and draw particles
        for particle in particles:
            particle['y'] += particle['speed']
            if particle['y'] > height:
                particle['y'] = 0
                particle['x'] = random.randint(0, width)
            
            size_variation = math.sin(animation_counter * 2 + particle['x']) * 2
            pygame.draw.circle(screen, particle['color'], 
                              (int(particle['x']), int(particle['y'])), 
                              int(particle['size'] + size_variation))
        
        # Draw title and UI elements
        draw_title(screen, width, height, assets['title_font'], 
                 assets['small_font'], animation_counter)
        draw_divider(screen, width, height)
        
        # Create buttons
        button_width = width // 2.5
        button_height = 80
        button_spacing = 40
        
        # Play button
        play_rect = pygame.Rect(
            (width - button_width) // 2,
            height * 2 // 3,
            button_width,
            button_height
        )
        
        # Check if mouse is over play button
        play_hover, play_button_rect = create_button(
            screen, play_rect, "Start Game", assets['button_font'],
            const.GOLD, const.ROYAL_BLUE,
            assets['piece_images'][0] if assets['piece_images'] else None,
            True, animation_counter
        )
        
        # Play hover sound once when entering button area
        if play_hover and not button_states['play']['hover'] and assets['hover_sound']:
            assets['hover_sound'].play()
        button_states['play']['hover'] = play_hover
        
        # Quit button
        quit_rect = pygame.Rect(
            (width - button_width) // 2,
            height * 2 // 3 + button_height + button_spacing,
            button_width,
            button_height
        )
        
        # Check if mouse is over quit button
        quit_hover, quit_button_rect = create_button(
            screen, quit_rect, "Quit Game", assets['button_font'],
            (180, 0, 0), const.DARK_RED,
            assets['piece_images'][2] if len(assets['piece_images']) > 2 else None,
            True, animation_counter
        )
        
        # Quit hover sound once when entering button area
        if quit_hover and not button_states['quit']['hover'] and assets['hover_sound']:
            assets['hover_sound'].play()
        button_states['quit']['hover'] = quit_hover
        
        pygame.display.flip()
        clock.tick(120)  # Cap at 120 FPS
    
    return "QUIT"