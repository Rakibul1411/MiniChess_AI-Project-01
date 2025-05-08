# difficulty_screen.py
import pygame
import os
import sys
import math
import random
import constants as const
from launch_screen import create_launch_screen

def initialize_chess_pieces(width, height, count=15):
    """Initialize falling chess pieces with random properties"""
    piece_types = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
    piece_colors = ['white', 'black']
    
    chess_pieces = []
    for _ in range(count):
        piece = {
            'x': random.randint(0, width),
            'y': random.randint(-500, -50),
            'speed': random.uniform(1, 3),
            'rotation': random.randint(0, 360),
            'rot_speed': random.uniform(-2, 2),
            'size': random.randint(30, 50),
            'type': random.choice(piece_types),
            'color': random.choice(piece_colors)
        }
        chess_pieces.append(piece)
    return chess_pieces

def update_chess_pieces(chess_pieces, width, height):
    """Update positions of falling chess pieces"""
    for piece in chess_pieces:
        piece['y'] += piece['speed']
        piece['rotation'] += piece['rot_speed']
        
        if piece['y'] > height + 50:
            piece['y'] = random.randint(-200, -50)
            piece['x'] = random.randint(0, width)
            piece['speed'] = random.uniform(1, 3)
            piece['type'] = random.choice(['pawn', 'knight', 'bishop', 'rook', 'queen', 'king'])
            piece['color'] = random.choice(['white', 'black'])

def load_assets(assets_dir):
    """Load all game assets (images, fonts, sounds)"""
    assets = {
        'bg_image': None,
        'piece_images': {},
        'fonts': {}
    }
    
    # Load background image
    try:
        bg_image = pygame.image.load(os.path.join(assets_dir, 'difficulty.png'))
        assets['bg_image'] = bg_image
    except:
        pass
    
    # Load chess piece images
    piece_types = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
    piece_colors = ['white', 'black']
    
    try:
        for color in piece_colors:
            for piece_type in piece_types:
                image_name = f"{color}_{piece_type}.png"
                image_path = os.path.join(assets_dir, image_name)
                if os.path.exists(image_path):
                    assets['piece_images'][f"{color}_{piece_type}"] = pygame.image.load(image_path)
                else:
                    assets['piece_images'][f"{color}_{piece_type}"] = None
    except:
        pass
    
    # Load fonts
    try:
        font_path = os.path.join(assets_dir, 'medieval.ttf')
        if os.path.exists(font_path):
            assets['fonts']['title'] = pygame.font.Font(font_path, 60)
            assets['fonts']['button'] = pygame.font.Font(font_path, 38)
            assets['fonts']['back'] = pygame.font.Font(font_path, 36)
            assets['fonts']['desc'] = pygame.font.Font(font_path, 22)
        else:
            assets['fonts']['title'] = pygame.font.SysFont("Arial", 60, bold=True)
            assets['fonts']['button'] = pygame.font.SysFont("Arial", 38, bold=True)  
            assets['fonts']['back'] = pygame.font.SysFont("Arial", 36)
            assets['fonts']['desc'] = pygame.font.SysFont("Arial", 22)
    except:
        assets['fonts']['title'] = pygame.font.SysFont("Arial", 60, bold=True) 
        assets['fonts']['button'] = pygame.font.SysFont("Arial", 38, bold=True)  
        assets['fonts']['back'] = pygame.font.SysFont("Arial", 36)
        assets['fonts']['desc'] = pygame.font.SysFont("Arial", 22)
    
    return assets

def draw_chess_piece(screen, piece, piece_images):
    """Draw a single chess piece with rotation"""
    piece_key = f"{piece['color']}_{piece['type']}"
    if piece_key in piece_images and piece_images[piece_key]:
        img = piece_images[piece_key]
        img = pygame.transform.scale(img, (piece['size'], piece['size']))
        img = pygame.transform.rotate(img, piece['rotation'])
        img_rect = img.get_rect(center=(piece['x'], piece['y']))
        screen.blit(img, img_rect.topleft)
    else:
        piece_color = const.WHITE if piece['color'] == 'white' else const.BLACK
        piece_border = const.BLACK if piece['color'] == 'white' else const.WHITE
        
        if piece['type'] == 'pawn':
            pygame.draw.circle(screen, piece_color, (int(piece['x']), int(piece['y'])), piece['size']//2)
            pygame.draw.circle(screen, piece_border, (int(piece['x']), int(piece['y'])), piece['size']//2, 2)
        elif piece['type'] == 'knight':
            points = []
            for i in range(5):
                angle = math.radians(piece['rotation'] + i * 72)
                points.append((
                    piece['x'] + piece['size']//2 * math.cos(angle),
                    piece['y'] + piece['size']//2 * math.sin(angle)
                ))
            pygame.draw.polygon(screen, piece_color, points)
            pygame.draw.polygon(screen, piece_border, points, 2)
        else:
            rect = pygame.Rect(0, 0, piece['size'], piece['size'])
            rect.center = (piece['x'], piece['y'])
            pygame.draw.rect(screen, piece_color, rect, border_radius=8)
            pygame.draw.rect(screen, piece_border, rect, 2, border_radius=8)

def create_gradient_button(surface, rect, base_color, hover=False):
    """Create a gradient button with hover effect"""
    if hover:
        base_color = (base_color[0] + 30, base_color[1] + 30, base_color[2] + 30)
    
    gradient = pygame.Surface((rect.width, rect.height))
    for i in range(rect.height):
        intensity = 1 - (i / rect.height) * 0.3
        color = (
            int(base_color[0] * intensity),
            int(base_color[1] * intensity),
            int(base_color[2] * intensity)
        )
        pygame.draw.line(gradient, color, (0, i), (rect.width, i))
    surface.blit(gradient, rect)
    
    # Add shiny edge effect
    pygame.draw.rect(surface, (255, 255, 255, 200), rect, 3, border_radius=10)
    return rect

def draw_title(screen, width, height, font, animation_timer):
    """Draw the animated title with glow effect"""
    pulse = math.sin(animation_timer) * 5
    title_text = font.render("SELECT DIFFICULTY", True, const.GOLD)
    title_rect = title_text.get_rect(center=(width//2, height//6 + pulse))
    
    glow_size = 10 + int((abs(math.sin(animation_timer * 2)) * 8))
    glow_surf = pygame.Surface((title_rect.width + glow_size, title_rect.height + glow_size), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (const.GOLD[0], const.GOLD[1], const.GOLD[2], 50), 
                         (0, 0, title_rect.width + glow_size, title_rect.height + glow_size), 
                         border_radius=20)
    screen.blit(glow_surf, (title_rect.x - glow_size//2, title_rect.y - glow_size//2))
    screen.blit(title_text, title_rect)

def draw_difficulty_button(screen, width, height, font, desc_font, 
                          y_pos, text, color, description):
    """Draw a difficulty selection button with description"""
    button_width = width // 2
    button_height = 70
    
    button_rect = pygame.Rect(
        (width - button_width) // 2,
        y_pos,
        button_width,
        button_height
    )
    
    mouse_pos = pygame.mouse.get_pos()
    hover = button_rect.collidepoint(mouse_pos)
    
    create_gradient_button(screen, button_rect, color, hover)
    
    # Determine text color based on button color brightness
    brightness = color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114
    text_color = const.BLACK if brightness > 150 else const.WHITE
    
    button_text = font.render(text, True, text_color)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    # Add description
    desc_text = desc_font.render(description, True, const.WHITE)
    desc_rect = desc_text.get_rect(center=(width//2, button_rect.bottom + 10))
    screen.blit(desc_text, desc_rect)
    
    return button_rect

def draw_back_button(screen, height, font):
    """Draw the back button with arrow icon"""
    button_rect = pygame.Rect(20, height - 70, 120, 50)
    mouse_pos = pygame.mouse.get_pos()
    hover = button_rect.collidepoint(mouse_pos)
    back_color = (180, 0, 0) if hover else (120, 0, 0)
    
    # Create gradient
    gradient = pygame.Surface((120, 50))
    for i in range(50):
        intensity = 1 - (i / 50) * 0.3
        color = (
            int(back_color[0] * intensity),
            int(back_color[1] * intensity),
            int(back_color[2] * intensity)
        )
        pygame.draw.line(gradient, color, (0, i), (120, i))
    screen.blit(gradient, button_rect)
    
    # Add border
    pygame.draw.rect(screen, const.WHITE, button_rect, 2, border_radius=10)
    
    # Arrow icon
    pygame.draw.polygon(screen, const.WHITE, [
        (button_rect.x + 20, button_rect.centery),
        (button_rect.x + 35, button_rect.y + 10),
        (button_rect.x + 35, button_rect.y + 40)
    ])
    
    back_text = font.render("Back", True, const.WHITE)
    back_text_rect = back_text.get_rect(center=(button_rect.centerx + 10, button_rect.centery))
    screen.blit(back_text, back_text_rect)
    
    return button_rect

def draw_footer(screen, width, height):
    """Draw the footer text"""
    footer_font = pygame.font.SysFont("Arial", 16)
    footer_text = footer_font.render("Select a difficulty level to start playing", True, (200, 200, 200))
    footer_rect = footer_text.get_rect(bottom=height-10, centerx=width//2)
    screen.blit(footer_text, footer_rect)
    
def play_click_sound(assets_dir):
    """Play button click sound if available"""
    try:
        sound_path = os.path.join(assets_dir, 'click.wav')
        if os.path.exists(sound_path):
            click_sound = pygame.mixer.Sound(sound_path)
            click_sound.play()
    except:
        pass

def create_difficulty_screen(screen, width, height):  
    """Main function to create and manage the difficulty selection screen"""
    # Initialize assets and game elements
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    assets = load_assets(assets_dir)
    
    # Scale background image if loaded
    if assets['bg_image']:
        assets['bg_image'] = pygame.transform.smoothscale(assets['bg_image'], (width, height))
    
    # Animation variables
    animation_timer = 0
    chess_pieces = initialize_chess_pieces(width, height)
    
    # Main loop for difficulty screen
    running = True
    clock = pygame.time.Clock()
    
    # Initialize button rects
    easy_button_rect = medium_button_rect = hard_button_rect = back_button_rect = None
    
    while running:
        animation_timer += 0.03
        update_chess_pieces(chess_pieces, width, height)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check button clicks
                if easy_button_rect and easy_button_rect.collidepoint(mouse_pos):
                    play_click_sound(assets_dir)
                    return "EASY"
                elif medium_button_rect and medium_button_rect.collidepoint(mouse_pos):
                    play_click_sound(assets_dir)
                    return "MEDIUM"
                elif hard_button_rect and hard_button_rect.collidepoint(mouse_pos):
                    play_click_sound(assets_dir)
                    return "HARD"
                elif back_button_rect and back_button_rect.collidepoint(mouse_pos):
                    play_click_sound(assets_dir)
                    choice = create_launch_screen(screen, width, height)
                    if choice == "PLAY":
                        return "BACK_TO_PLAY"
                    else:
                        pygame.quit()
                        sys.exit()
        
        # Draw background
        if assets['bg_image']:
            screen.blit(assets['bg_image'], (0, 0))
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
        else:
            for i in range(height):
                color = (0, 0, 50 + int(50 * i/height))
                pygame.draw.line(screen, color, (0, i), (width, i))
        
        # Draw chess pieces
        for piece in chess_pieces:
            draw_chess_piece(screen, piece, assets['piece_images'])
        
        # Draw UI elements
        draw_title(screen, width, height, assets['fonts']['title'], animation_timer)
        
        button_spacing = 50
        button_height = 70
        start_y = height * 2 // 5
        
        # Draw difficulty buttons
        easy_button_rect = draw_difficulty_button(
            screen, width, height, 
            assets['fonts']['button'], assets['fonts']['desc'],
            start_y, "Easy", const.BRONZE, 
            "For beginners - AI makes basic moves"
        )
        
        medium_button_rect = draw_difficulty_button(
            screen, width, height, 
            assets['fonts']['button'], assets['fonts']['desc'],
            start_y + button_height + button_spacing, "Medium", const.SILVER,
            "For casual players - AI has moderate strategy"
        )
        
        hard_button_rect = draw_difficulty_button(
            screen, width, height, 
            assets['fonts']['button'], assets['fonts']['desc'],
            start_y + 2*(button_height + button_spacing), "Hard", const.GOLD,
            "For experts - AI uses advanced tactics"
        )
        
        # Draw back button and footer
        back_button_rect = draw_back_button(screen, height, assets['fonts']['back'])
        draw_footer(screen, width, height)
        
        pygame.display.flip()
        clock.tick(120)
    
    return "EASY"  # Default return if loop exits unexpectedly