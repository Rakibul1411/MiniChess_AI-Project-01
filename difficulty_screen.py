# difficulty_screen.py
import pygame
import os
import sys
import math
import random
import constants as const
from launch_screen import create_launch_screen
from draw_title_button import draw_title, draw_button_with_description, draw_back_button

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
        'fonts': {},
        'hover_sound': None,
        'click_sound': None
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
        title_font_path = os.path.join(assets_dir, 'Bassy.ttf')
        button_font_path = os.path.join(assets_dir, 'Rosemary.ttf')
        desc_font_path = os.path.join(assets_dir, 'Handsean.ttf')
        
        if os.path.exists(title_font_path):
            assets['fonts']['title'] = pygame.font.Font(title_font_path, 60)
        else:
            assets['fonts']['title'] = pygame.font.SysFont("Times New Roman", 60, bold=True)
            
        if os.path.exists(button_font_path):
            assets['fonts']['button'] = pygame.font.Font(button_font_path, 25)
            assets['fonts']['back'] = pygame.font.Font(button_font_path, 25)
        else:
            assets['fonts']['button'] = pygame.font.SysFont("Georgia", 25, bold=True)
            assets['fonts']['back'] = pygame.font.SysFont("Georgia", 25)
            
        if os.path.exists(desc_font_path):
            assets['fonts']['desc'] = pygame.font.Font(desc_font_path, 20)
        else:
            assets['fonts']['desc'] = pygame.font.SysFont("Georgia", 20)
    except:
        assets['fonts']['title'] = pygame.font.SysFont("Times New Roman", 60, bold=True)
        assets['fonts']['button'] = pygame.font.SysFont("Georgia", 25, bold=True)
        assets['fonts']['back'] = pygame.font.SysFont("Georgia", 25)
        assets['fonts']['desc'] = pygame.font.SysFont("Georgia", 20)
    
    # Load sounds
    try:
        pygame.mixer.init()
        assets['hover_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'hover.mp3'))
        assets['click_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'click.wav'))
    except:
        pass
    
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
    
    # Button states for hover sound
    button_states = {
        'easy': {'hover': False},
        'medium': {'hover': False},
        'hard': {'hover': False},
        'back': {'hover': False}
    }
    
    # Main loop for difficulty screen
    running = True
    clock = pygame.time.Clock()
    
    # Initialize button rects
    easy_button_rect = medium_button_rect = hard_button_rect = back_button_rect = None
    
    while running:
        animation_timer += 0.03
        update_chess_pieces(chess_pieces, width, height)
        
        # Get mouse position for cursor handling
        mouse_pos = pygame.mouse.get_pos()
        any_hover = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_button_rect and easy_button_rect.collidepoint(mouse_pos):
                    if assets['click_sound']:
                        assets['click_sound'].play()
                    return "EASY"
                elif medium_button_rect and medium_button_rect.collidepoint(mouse_pos):
                    if assets['click_sound']:
                        assets['click_sound'].play()
                    return "MEDIUM"
                elif hard_button_rect and hard_button_rect.collidepoint(mouse_pos):
                    if assets['click_sound']:
                        assets['click_sound'].play()
                    return "HARD"
                elif back_button_rect and back_button_rect.collidepoint(mouse_pos):
                    if assets['click_sound']:
                        assets['click_sound'].play()
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
        easy_button_rect = draw_button_with_description(
            screen, width, height, 
            assets['fonts']['button'], assets['fonts']['desc'],
            start_y, "Easy", const.BRONZE, 
            "For beginners - AI makes basic moves",
            button_states, 'easy', assets
        )
        
        medium_button_rect = draw_button_with_description(
            screen, width, height, 
            assets['fonts']['button'], assets['fonts']['desc'],
            start_y + button_height + button_spacing, "Medium", const.SILVER,
            "For casual players - AI has moderate strategy",
            button_states, 'medium', assets
        )
        
        hard_button_rect = draw_button_with_description(
            screen, width, height, 
            assets['fonts']['button'], assets['fonts']['desc'],
            start_y + 2*(button_height + button_spacing), "Hard", const.GOLD,
            "For experts - AI uses advanced tactics",
            button_states, 'hard', assets
        )
        
        # Draw back button
        back_button_rect = draw_back_button(screen, height, assets['fonts']['back'], button_states, assets)
        
        # Check hover states for cursor
        any_hover = (easy_button_rect.collidepoint(mouse_pos) or 
                    medium_button_rect.collidepoint(mouse_pos) or 
                    hard_button_rect.collidepoint(mouse_pos) or 
                    back_button_rect.collidepoint(mouse_pos))
        
        # Set cursor based on hover state
        if any_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        pygame.display.flip()
        clock.tick(120)
    
    return "EASY"  # Default return if loop exits unexpectedly